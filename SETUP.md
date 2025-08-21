# ReflexEngine Development Setup

This document provides guidance for setting up a development environment for ReflexEngine.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JohnVonChaos/ReflexEngine.git
   cd ReflexEngine
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```
   FIREWORKS_API_KEY=your_api_key_here
   CONSCIOUS_MODEL=accounts/fireworks/models/llama4-maverick-instruct-basic
   SUBCONSCIOUS_MODEL=accounts/fireworks/models/llama4-scout-instruct-basic
   DEBUG_MODE=false
   ```

4. **Run the application:**
   ```bash
   python ReflexEngine_SelfPublished_v1.py
   ```

## System Dependencies

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

### CentOS/RHEL
```bash
sudo yum install tkinter
```

### macOS
```bash
# If using Homebrew
brew install python-tk
```

## Development Workflow

### Running Tests
```bash
# Currently requires GUI mock setup
python -m unittest tests.test_fibonacci_semantic_spiral -v
```

### Code Analysis
See `STRUCTURAL_ANALYSIS.md` for detailed code structure analysis and improvement recommendations.

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'tkinter'**
   - Install tkinter system package (see System Dependencies above)

2. **FIREWORKS_API_KEY not set error**
   - Ensure `.env` file exists and contains your API key
   - Check that python-dotenv is installed

3. **Import errors in tests**
   - Tests currently have dependency issues due to monolithic architecture
   - See STRUCTURAL_ANALYSIS.md for recommended fixes

## Project Structure

```
ReflexEngine/
├── ReflexEngine_SelfPublished_v1.py  # Main application (monolithic)
├── tests/
│   └── test_fibonacci_semantic_spiral.py
├── requirements.txt                   # Python dependencies
├── SETUP.md                          # This file
├── STRUCTURAL_ANALYSIS.md            # Code analysis and recommendations
├── README.md                         # Project description
├── LICENSE.txt                       # License information
├── crystal.json                      # Memory persistence file
├── stm.json                         # Short-term memory persistence
└── .env                             # Environment variables (create this)
```

## Next Steps

For improved development experience, consider implementing the recommendations in `STRUCTURAL_ANALYSIS.md`, particularly:

1. **Modular refactoring** - Break down the monolithic file
2. **Configuration management** - Centralize settings
3. **Testing infrastructure** - Create proper test isolation
4. **Error handling** - Add comprehensive logging

## Contributing

When making changes:
1. Read `STRUCTURAL_ANALYSIS.md` to understand current issues
2. Make minimal, focused changes
3. Test your changes thoroughly
4. Consider impact on existing functionality

## Security Notes

- Never commit your `.env` file with real API keys
- The current codebase may expose sensitive information in debug output
- Review STRUCTURAL_ANALYSIS.md for security recommendations