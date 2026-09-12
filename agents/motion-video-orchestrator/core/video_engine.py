"""
Motion Video & Remotion Graphics Orchestrator Engine.
Compiles programmatic React/Remotion motion graphic sequences, kinetic typography, and storyboard manifests.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json


@dataclass
class VideoScene:
    id: int
    duration_frames: int  # 30 fps
    title: str
    subtitle: str
    transition: str  # "fade", "slide-up", "wipe", "zoom-in"
    color_scheme: Dict[str, str]


@dataclass
class MotionProjectManifest:
    project_name: str
    fps: int
    width: int
    height: int
    total_frames: int
    total_duration_sec: float
    scenes: List[VideoScene]
    remotion_composition_jsx: str


class MotionVideoEngine:
    """Generates broadcast-quality Remotion video compositions and scenes."""

    @classmethod
    def compile_project(
        cls,
        title: str,
        script_bullets: List[str],
        fps: int = 30,
        width: int = 1920,
        height: int = 1080
    ) -> MotionProjectManifest:
        scenes: List[VideoScene] = []
        scene_duration = 90  # 3 seconds per scene at 30 fps

        palettes = [
            {"bg": "#0a0a0f", "primary": "#00f0ff", "text": "#ffffff"},
            {"bg": "#0f0c1b", "primary": "#ff0055", "text": "#f1f2f6"},
            {"bg": "#050e14", "primary": "#00ff88", "text": "#ffffff"},
        ]

        for idx, bullet in enumerate(script_bullets, 1):
            p = palettes[(idx - 1) % len(palettes)]
            scenes.append(VideoScene(
                id=idx,
                duration_frames=scene_duration,
                title=f"Scene {idx}",
                subtitle=bullet,
                transition="slide-up" if idx % 2 == 0 else "zoom-in",
                color_scheme=p
            ))

        total_frames = len(scenes) * scene_duration
        total_sec = total_frames / fps

        # Generate Remotion React JSX composition
        jsx_code = f"""import {{ Composition, Sequence, interpolate, useCurrentFrame }} from 'remotion';

export const {title.replace(' ', '')}Video = () => {{
  return (
    <div style={{{{ flex: 1, backgroundColor: '#090a0f', color: '#fff' }}}}>
"""
        for s in scenes:
            start_f = (s.id - 1) * s.duration_frames
            jsx_code += f"""      <Sequence from={{{start_f}}} durationInFrames={{{s.duration_frames}}}>
        <div style={{{{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%' }}}}>
          <h1 style={{{{ fontSize: 72, color: '{s.color_scheme["primary"]}', margin: 0 }}}}>{s.title}</h1>
          <p style={{{{ fontSize: 36, maxWidth: 1200, textAlign: 'center' }}}}>{s.subtitle}</p>
        </div>
      </Sequence>
"""
        jsx_code += """    </div>
  );
};
"""

        return MotionProjectManifest(
            project_name=title,
            fps=fps,
            width=width,
            height=height,
            total_frames=total_frames,
            total_duration_sec=total_sec,
            scenes=scenes,
            remotion_composition_jsx=jsx_code
        )
