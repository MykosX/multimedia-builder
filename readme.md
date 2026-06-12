
## Multimedia Builder (JSON-driven Multimedia Pipeline Engine)

## Overview

Multimedia Builder is a configuration-driven pipeline system for processing audio, image, video and text using modular handlers.

The system is fully controlled by a central `manager.json` file that defines which pipelines are enabled and executed.

Pipelines are executed sequentially based on configuration in `manager.json`.

Each pipeline contains structured activities. Each activity groups related actions, and each action represents an executable command handled by internal framework modules.

Activities group related actions under a common task context. Actions are the smallest executable unit in the system.

## Execution Model

The system executes in four hierarchical levels:

### 1. Manager level
The `manager.json` file controls which pipelines are executed.

Example:

```json
{
  "project-title": "Describe Techniques",
  "pipelines": [
    {
      "path": "pipelines/sample-audio.json",
      "enabled": true
    },
    {
      "path": "pipelines/sample-image.json",
      "enabled": false
    }
  ]
}
```
Only pipelines with `"enabled": true` are loaded and executed.

### 2. Pipeline level
Each pipeline file defines a set of activities.

Example:

```json
{
  "subproject-title": "Work on audio activities",
  "activities": [
    {
      "name": "Prepare speech files",
      "type": "tts",
      "defaults": {
        "model-path": "tts_models/en/ljspeech/vits"
      },
      "actions": [
        {
          "command": "text-to-speech",
          "enabled": true,
          "text": "Hello world",
          "output-audio-path": "output/audio/example.wav"
        }
      ]
    }
  ]
}
```

### 3. Activity level
Each activity contains a list of actions (commands).

Activities group related actions under a common task context.

### 4. Action level
Actions represent executable commands inside an activity.

Each action contains:
- `command`: the operation to execute
- `enabled`: whether it runs or not
- additional parameters depending on the command type

Actions map to executable commands handled by internal framework modules.

Example commands:
- text-to-speech
- audio-to-text
- create-silence
- combine-audios
- split-audio

## Execution Flow

1. Load `manager.json`
2. Filter pipelines where `enabled = true`
3. Load each pipeline file
4. Iterate through activities
5. For each activity, execute enabled actions sequentially (in defined order)

---

## Requirements

 - Python **3.11.x**
 - FFmpeg
 - eSpeak
 - GNU Make

---

## Supported Platforms

### Tested:
 - Ubuntu 22.04 LTS
 - Fedora
 - WSL2 (Ubuntu 22.04 LTS)

### Recommended setup:
 - Windows users must use WSL2 (Ubuntu 22.04 LTS)

### Not officially supported:
 - Native Windows (without WSL)
 - macOS (untested)

---

## Development Workflow

The project is designed to run in a Linux-like environment.

### Recommended directory structure (inside WSL):

```bash
~/projects/multimedia-builder
```

### Editing options:
 - VS Code (recommended) via WSL extension
 - PyCharm (WSL interpreter)
 - Notepad++ via \\wsl$\Ubuntu\home\<user>\projects

### Execution environment:
All execution happens inside WSL/Linux environment.
Windows is used only as a UI layer.

---

## System dependencies
### Ubuntu / WSL

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y ffmpeg espeak-ng make python3.11 python3.11-dev python3.11-venv
```

### Fedora

```bash
sudo dnf install -y ffmpeg espeak-ng make python3
```

---

## Quick Start

### 1. Clone repository

```bash
git clone https://github.com/MykosX/multimedia-builder.git
cd multimedia-builder
```

### 2. Setup Environment

```bash
make setup
```
This will:
 - create a virtual environment
 - install Python dependencies from requirements.txt

### 3. Run project

```bash
make run
```

### 4. Check dependencies

```bash
make check
```

### 5. Project info

```bash
make info
```

---

## Project Structure

Here is a brief overview of the project structure:

```
project-root/
├── Makefile                    # Build and runtime commands
├── runner.py                   # Entry point for execution
├── manager.json                # Controls active pipelines
├── core/
│   ├── frameworks/             # Command handlers (TTS, audio, video, etc.)
│   ├── utils/                  # Helpers (logging, file handling)
│   └── manager.py              # Pipeline execution engine
├── pipelines/
│   ├── sample-audio.json
│   ├── sample-image.json
│   ├── sample-translate.json
│   └── sample-video.json
├── requirements.txt
└── README.md
└── LICENSE
```

---

## Notes
 - The system is Linux-first and WSL-compatible.
 - Running directly on native Windows is not supported.
 - File system performance is optimal when the project resides inside the Linux filesystem (WSL ext4).

---

## License

See the LICENSE file for details.
