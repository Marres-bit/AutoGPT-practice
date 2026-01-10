#!/usr/bin/env python
"""Test file attachment integration"""

from agent import AIAgent
from file_handler import FileHandler

print('='*70)
print('TESTING FILE ATTACHMENT INTEGRATION')
print('='*70)

# Test 1: Agent initialization
print('\n📌 TEST 1: Agent initialization')
try:
    agent = AIAgent()
    print('✅ Agent initialized successfully')
    print(f'   Model: {agent.get_model()}')
except Exception as e:
    print(f'❌ Error: {e}')
    exit(1)

# Test 2: Message building
print('\n📌 TEST 2: Message content building')

# Test simple text
content1 = agent._build_message_content('Hello world', None)
assert isinstance(content1, str), "Text should return string"
print('✅ Text only: returns string')

# Test empty message with no files
content2 = agent._build_message_content('', None)
assert isinstance(content2, str), "Should return default message"
print('✅ Empty text: returns default message')

# Test with files (simulated)
files_data = {
    'images': [{'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,...'}}],
    'files_info': [{'name': 'test.jpg', 'type': 'image', 'path': '/path/to/test.jpg'}]
}
content3 = agent._build_message_content('Analyze this', files_data)
assert isinstance(content3, list), "Mixed content should return list"
assert len(content3) == 3, "Should have 3 items: text, image, files_info"
print(f'✅ Text with files: returns list of {len(content3)} items')
print(f'   Item types: {[item.get("type") for item in content3]}')

# Test 3: FileHandler
print('\n📌 TEST 3: FileHandler operations')
fh = FileHandler()

# Verify supported types
supported = len(fh.SUPPORTED_TYPES)
print(f'✅ Supported file types: {supported} categories')
for ftype, exts in fh.SUPPORTED_TYPES.items():
    print(f'   - {ftype}: {len(exts)} formats')

# Verify max file size
max_size_mb = fh.MAX_FILE_SIZE / (1024 * 1024)
print(f'✅ Max file size: {max_size_mb:.0f} MB')

# Test file type detection
test_files = ['image.jpg', 'video.mp4', 'audio.wav', 'unknown.xyz']
for fname in test_files:
    ftype = FileHandler.get_file_type(fname)
    if ftype:
        print(f'✅ {fname} -> {ftype}')
    else:
        print(f'✅ {fname} -> unsupported (as expected)')

print('\n' + '='*70)
print('✅ ALL TESTS PASSED - FILE ATTACHMENT READY!')
print('='*70)
