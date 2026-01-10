"""
File Handler - Manage media uploads and preprocessing
Supports images, videos, and audio files with REAL processing:
- Images: Base64 encoding for Vision API
- Audio: Whisper API transcription
- Video: Frame extraction + audio transcription
"""
import os
import base64
import subprocess
import tempfile
from pathlib import Path
from typing import List, Tuple, Dict, Optional

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False


class FileHandler:
    """Handle file uploads, validation, and encoding"""
    
    # Supported file types
    SUPPORTED_TYPES = {
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'],
        'video': ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv'],
        'audio': ['.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac'],
        'document': ['.pdf', '.txt', '.docx', '.xlsx', '.pptx']
    }
    
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
    
    def __init__(self, openai_client=None):
        self.selected_files = []
        # Import here to avoid circular imports
        from openai import OpenAI
        self.client = openai_client or OpenAI()
    
    @staticmethod
    def get_file_type(file_path: str) -> Optional[str]:
        """Determine file type from extension"""
        ext = Path(file_path).suffix.lower()
        for file_type, extensions in FileHandler.SUPPORTED_TYPES.items():
            if ext in extensions:
                return file_type
        return None
    
    @staticmethod
    def is_valid_file(file_path: str) -> Tuple[bool, str]:
        """
        Validate file exists and is supported
        Returns (is_valid, error_message)
        """
        if not os.path.exists(file_path):
            return False, "Fichier introuvable"
        
        file_type = FileHandler.get_file_type(file_path)
        if not file_type:
            ext = Path(file_path).suffix
            return False, f"Type de fichier non supporté: {ext}"
        
        file_size = os.path.getsize(file_path)
        if file_size > FileHandler.MAX_FILE_SIZE:
            size_mb = file_size / (1024 * 1024)
            return False, f"Fichier trop volumineux ({size_mb:.1f} MB > 100 MB)"
        
        return True, ""
    
    def validate_file(self, file_path: str) -> Tuple[bool, str]:
        """Instance method wrapper for is_valid_file"""
        return self.is_valid_file(file_path)
    
    @staticmethod
    def encode_image_to_base64(file_path: str) -> Optional[str]:
        """
        Encode image to base64 for OpenAI Vision API
        
        Args:
            file_path (str): Path to image file
            
        Returns:
            str: Base64 encoded image data or None if error
        """
        try:
            with open(file_path, "rb") as image_file:
                return base64.standard_b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None
    
    @staticmethod
    def get_image_media_type(file_path: str) -> str:
        """Get MIME type for image"""
        ext = Path(file_path).suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        return mime_types.get(ext, 'image/jpeg')
    
    def add_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Add file to selected files list
        
        Args:
            file_path (str): Path to file to add
            
        Returns:
            (success: bool, message: str)
        """
        is_valid, error_msg = self.is_valid_file(file_path)
        if not is_valid:
            return False, error_msg
        
        # Check if already added
        if file_path in [f['path'] for f in self.selected_files]:
            return False, "Fichier déjà sélectionné"
        
        file_type = self.get_file_type(file_path)
        file_name = Path(file_path).name
        file_size = os.path.getsize(file_path)
        
        self.selected_files.append({
            'path': file_path,
            'name': file_name,
            'type': file_type,
            'size': file_size,
            'icon': self._get_icon(file_type)
        })
        
        return True, f"✓ {file_name} ajouté"
    
    def remove_file(self, file_path: str) -> bool:
        """Remove file from selected files"""
        self.selected_files = [f for f in self.selected_files if f['path'] != file_path]
        return True
    
    def clear_files(self):
        """Clear all selected files"""
        self.selected_files = []
    
    def get_selected_files(self) -> List[Dict]:
        """Get list of selected files"""
        return self.selected_files
    
    def get_file_display_text(self) -> str:
        """Get formatted text for displaying selected files"""
        if not self.selected_files:
            return ""
        
        lines = ["📎 Fichiers joints:"]
        for file_info in self.selected_files:
            icon = file_info['icon']
            name = file_info['name']
            size_kb = file_info['size'] / 1024
            size_str = f"{size_kb:.0f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
            lines.append(f"  {icon} {name} ({size_str})")
        
        return "\n".join(lines)
    
    # ==================== AUDIO PROCESSING ====================
    
    def process_audio(self, file_path: str) -> Optional[str]:
        """
        Process audio using Whisper API for transcription
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Transcribed text or None if error
        """
        try:
            print(f"🎵 Transcribing audio: {Path(file_path).name}...")
            
            with open(file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="fr"
                )
            
            text = transcript.text
            print(f"✅ Audio transcribed: {len(text)} characters")
            return text
            
        except Exception as e:
            print(f"❌ Error transcribing audio: {e}")
            return None
    
    # ==================== VIDEO PROCESSING ====================
    
    def extract_video_frames(self, file_path: str, num_frames: int = 3) -> Optional[List[Dict]]:
        """
        Extract frames from video and encode as images
        
        Args:
            file_path: Path to video file
            num_frames: Number of frames to extract
            
        Returns:
            List of Vision API image dicts or None
        """
        if not OPENCV_AVAILABLE:
            print("⚠️  opencv-python not installed. Falling back to audio extraction...")
            return None
        
        try:
            print(f"🎥 Extracting {num_frames} frames from video...")
            
            # Open video
            cap = cv2.VideoCapture(file_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if total_frames == 0:
                print("❌ Could not read video")
                cap.release()
                return None
            
            # Calculate frame intervals
            frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]
            
            frames_data = []
            temp_dir = tempfile.mkdtemp()
            
            for idx, frame_num in enumerate(frame_indices):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()
                
                if ret:
                    # Save frame temporarily
                    frame_path = os.path.join(temp_dir, f"frame_{idx}.jpg")
                    cv2.imwrite(frame_path, frame)
                    
                    # Encode to Vision API format
                    image_data = self._encode_image_to_vision_api(frame_path)
                    if image_data:
                        frames_data.append(image_data)
                    
                    # Clean up temp file
                    try:
                        os.remove(frame_path)
                    except:
                        pass
            
            cap.release()
            
            if frames_data:
                print(f"✅ Extracted {len(frames_data)} video frames")
            
            return frames_data if frames_data else None
            
        except Exception as e:
            print(f"❌ Error extracting video frames: {e}")
            return None
    
    def _encode_image_to_vision_api(self, file_path: str) -> Optional[Dict]:
        """Encode single image to Vision API format"""
        b64_data = self.encode_image_to_base64(file_path)
        if not b64_data:
            return None
        media_type = self.get_image_media_type(file_path)
        return {
            'type': 'image_url',
            'image_url': {
                'url': f"data:{media_type};base64,{b64_data}"
            }
        }
    
    def _extract_video_audio(self, file_path: str) -> Optional[str]:
        """
        Fallback: Extract and transcribe audio from video
        
        Args:
            file_path: Path to video file
            
        Returns:
            Transcribed audio text or None
        """
        try:
            print("🎵 Extracting audio from video...")
            
            # Create temp audio file
            temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_audio_path = temp_audio.name
            temp_audio.close()
            
            # Extract audio using ffmpeg
            cmd = [
                'ffmpeg',
                '-i', file_path,
                '-q:a', '9',
                '-n',
                temp_audio_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(temp_audio_path):
                # Transcribe extracted audio
                text = self.process_audio(temp_audio_path)
                
                # Clean up
                try:
                    os.remove(temp_audio_path)
                except:
                    pass
                
                return text
            
            return None
            
        except Exception as e:
            print(f"❌ Error extracting video audio: {e}")
            return None
    
    def process_video(self, file_path: str) -> Optional[Dict]:
        """
        Process video by extracting frames and/or audio
        
        Returns:
            Dict with 'frames' (images) and 'audio_text' (transcription)
        """
        result = {'frames': None, 'audio_text': None, 'file_name': Path(file_path).name}
        
        # Try to extract frames
        frames = self.extract_video_frames(file_path, num_frames=3)
        if frames:
            result['frames'] = frames
        
        # Try to extract audio
        audio_text = self._extract_video_audio(file_path)
        if audio_text:
            result['audio_text'] = audio_text
        
        return result if (result['frames'] or result['audio_text']) else None
    
    # ==================== MAIN FILE PROCESSING ====================
    
    def prepare_files_for_api(self) -> Dict:
        """
        REAL FILE PROCESSING:
        - Images: Encode to Vision API
        - Audio: Transcribe with Whisper
        - Video: Extract frames + transcribe audio
        
        Returns dict ready for API consumption
        """
        prepared = {
            'images': [],          # For Vision API
            'audio_texts': [],     # Transcribed audio
            'video_descriptions': [],  # Video analysis
            'files_info': [],      # Metadata
            'text_content': []     # All transcribed/readable content
        }
        
        for file_info in self.selected_files:
            file_type = file_info['type']
            file_path = file_info['path']
            file_name = file_info['name']
            
            print(f"\n🔄 Processing {file_type}: {file_name}")
            
            if file_type == 'image':
                # Process image for Vision API
                image_data = self._encode_image_to_vision_api(file_path)
                if image_data:
                    prepared['images'].append(image_data)
                    prepared['text_content'].append(f"[IMAGE] {file_name}")
            
            elif file_type == 'audio':
                # Transcribe audio with Whisper
                audio_text = self.process_audio(file_path)
                if audio_text:
                    prepared['audio_texts'].append(audio_text)
                    prepared['text_content'].append(
                        f"📄 TRANSCRIPTION AUDIO - {file_name}:\n{audio_text}"
                    )
            
            elif file_type == 'video':
                # Extract frames and audio from video
                video_data = self.process_video(file_path)
                if video_data:
                    if video_data.get('frames'):
                        prepared['images'].extend(video_data['frames'])
                    
                    if video_data.get('audio_text'):
                        prepared['video_descriptions'].append({
                            'file': file_name,
                            'audio': video_data['audio_text']
                        })
                        prepared['text_content'].append(
                            f"📹 TRANSCRIPTION VIDÉO - {file_name}:\n{video_data['audio_text']}"
                        )
            
            # Store file info for all types
            prepared['files_info'].append({
                'name': file_name,
                'type': file_type,
                'path': file_path
            })
        
        return prepared
    
    @staticmethod
    def _get_icon(file_type: str) -> str:
        """Get emoji icon for file type"""
        icons = {
            'image': '🖼️',
            'video': '🎥',
            'audio': '🎵',
            'document': '📄'
        }
        return icons.get(file_type, '📎')
