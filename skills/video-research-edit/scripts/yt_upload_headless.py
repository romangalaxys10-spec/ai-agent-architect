#!/usr/bin/env python3
"""yt_upload_headless.py — upload a video to the logged-in YouTube channel through a
dedicated HEADLESS Firefox (marionette port 2829) with pre-injected session cookies.
Usage:
  python3 yt_upload_headless.py --video final.mp4 --title-file t.txt \
      --description-file d.txt [--timeout-minutes 25]
Prereq (one-time per session):
  1. User's Firefox running with marionette on 2828 AND logged into YouTube
  2. Headless instance:  open -na /Applications/Firefox.app --args -marionette -no-remote \
        -profile <dir> -headless     (profile user.js: marionette.port=2829)
  3. Cookies harvested+injected (see SKILL.md)
"""
from marionette_driver.marionette import Marionette
import argparse, datetime, os, sys, time

def log(*a):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}]", *a, flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--title-file", required=True)
    ap.add_argument("--description-file", required=True)
    ap.add_argument("--timeout-minutes", type=int, default=25)
    ap.add_argument("--port", type=int, default=2829)
    args = ap.parse_args()
    title = open(args.title_file).read().strip()
    desc = open(args.description_file).read().strip()
    deadline = time.time() + args.timeout_minutes * 60

    m = Marionette(host="127.0.0.1", port=args.port)
    m.start_session()
    m.navigate("https://studio.youtube.com")
    time.sleep(12)

    r = m.execute_script("""
      const b=[...document.querySelectorAll('button, [role=button]')].find(e=>
        /create/i.test(e.getAttribute('aria-label')||'') && e.getBoundingClientRect().width>0);
      if (b) { b.click(); return 'create'; } return 'no create button';
    """)
    log(r); time.sleep(2.5)
    r = m.execute_script("""
      const items=[...document.querySelectorAll('tp-yt-paper-item, [role=menuitem], a, button')];
      const up=items.find(e=>/upload videos/i.test(e.innerText||'') && e.getBoundingClientRect().width>0);
      if (up) { up.click(); return 'upload-menu'; } return 'no menu item';
    """)
    log(r); time.sleep(7)
    n = m.execute_script("return document.querySelectorAll('input[type=file]').length")
    if not n:
        log("no file input — aborting"); sys.exit(1)
    m.execute_script("""
      const i=document.querySelector('input[type=file]');
      i.style.cssText='display:block !important;visibility:visible !important;opacity:1 !important;position:fixed;top:0;left:0;width:400px;height:60px;z-index:99999;';
    """)
    m.find_element("css selector", 'input[type=file]').send_keys(os.path.abspath(args.video))
    log("file attached:", os.path.basename(args.video))
    time.sleep(20)

    # metadata
    m.execute_script("""
      const tb=document.querySelector('#title-textarea');
      const ed=tb?(tb.querySelector('div[contenteditable=true]')||tb.querySelector('input')||tb):null;
      if (ed){ed.focus();ed.innerText='';document.execCommand('insertText',false,arguments[0]);}
    """, [title])
    time.sleep(1)
    m.execute_script("""
      const tb=document.querySelector('#description-textarea');
      const ed=tb?(tb.querySelector('div[contenteditable=true]')||tb):null;
      if (ed){ed.focus();ed.innerText='';document.execCommand('insertText',false,arguments[0]);}
    """, [desc])
    time.sleep(1)
    log("title+description filled")
    m.execute_script("""
      const el=[...document.querySelectorAll('tp-yt-paper-radio-button, [role=radio], div[role=radio]')]
        .find(e=>/not made for kids/i.test(e.innerText||''));
      if (el) el.click();
      else { const l=[...document.querySelectorAll('*')].find(e=>e.childElementCount===0&&/not made for kids/i.test(e.innerText||'')); if (l) l.click(); }
    """)
    log("not-made-for-kids selected")

    # wait for upload completion (Next enabled AND 'Uploading NN%' gone)
    while time.time() < deadline:
        st = m.execute_script("""
          const busy=/Uploading \\d+%/.test(document.body.innerText);
          const b=document.querySelector('#next-button');
          return JSON.stringify({busy, ready: b?!b.disabled:false});
        """)
        import json; j = json.loads(st)
        if not j["busy"] and j["ready"]:
            log("upload complete — proceeding"); break
        time.sleep(20)
    else:
        log("TIMEOUT waiting for upload"); sys.exit(2)

    for step in range(3):
        m.execute_script("const b=document.querySelector('#next-button'); if (b && !b.disabled) b.click();")
        time.sleep(4)
    log("through details/checks")
    r = m.execute_script("""
      const pub=[...document.querySelectorAll('tp-yt-paper-radio-button, [role=radio]')]
        .find(e=>/\\bpublic\\b/i.test(e.innerText||'') && e.getBoundingClientRect().width>0);
      if (pub) { pub.click(); return 'public'; } return 'public radio missing';
    """)
    log(r); time.sleep(2)
    r = m.execute_script("""
      const b=document.querySelector('#done-button');
      if (b && !b.disabled) { b.click(); return 'PUBLISHED'; } return 'publish blocked';
    """)
    log(r)
    if r != "PUBLISHED": sys.exit(3)
    time.sleep(12)
    # verify via content list
    m.navigate(f"https://studio.youtube.com/videos/upload")
    time.sleep(12)
    head = m.execute_script("""
      const r=document.querySelector('ytcp-video-row');
      return r? (r.innerText||'').split('\\n').slice(0,2).join(' / ').slice(0,90) : 'no rows';
    """)
    log("newest video row:", head)
    m.close()

if __name__ == "__main__":
    main()
