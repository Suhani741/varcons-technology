# Luminous - AI-Based Wallpaper Creation Tool

Luminous is a web application that allows users to create unique wallpapers using artificial intelligence. Users can describe their desired wallpaper by choosing colors, styles, and moods, and the system generates a custom wallpaper based on that input.

## Features

- **Color Selection:** Choose from VIBGYOR colors (Violet, Indigo, Blue, Green, Yellow, Orange, Red) to match different moods and designs.
- **Style & Mood:** Select design styles (e.g., abstract, nature) and moods (e.g., calm, energetic).
- **Text Description:** Add a short description to further customize the wallpaper.
- **Wallpaper Preview:** See a sample preview before downloading.
- **Easy-to-Use Interface:** Responsive design for desktop and mobile.
- **AI Image Generation (Pluggable):** The backend is ready for integration with AI models for image generation.

> **Note:** The current version uses placeholder images for previews and downloads. Integration with actual AI image generation is planned.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/luminous.git
   cd luminous
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   venv\Scripts\activate   # On Windows
   # source venv/bin/activate   # On macOS/Linux
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Start the server:**
   ```sh
   python app/main.py
   ```
   Or with Uvicorn:
   ```sh
   uvicorn app.main:app --reload
   ```

2. **Open your browser and go to:**
   ```
   http://localhost:8000
   ```

3. **Generate wallpapers:**
   - Fill out the form with your preferred color, style, mood, and description.
   - Submit to start wallpaper generation.
   - Preview and download your custom wallpaper.

## Project Structure

```
Wallpaper/
├── app/
│   ├── main.py
│   ├── static/
│   └── templates/
├── requirements.txt
└── README.md
```

## Requirements

See [`requirements.txt`](requirements.txt) for all dependencies.

## Customization & AI Integration

- The backend is structured to support AI-based image generation.
- To integrate your own AI model, replace the placeholder image generation logic in `app/main.py` with your model inference code.

## License

This project is licensed under the MIT License.

---

**Luminous** makes it easy for anyone to create beautiful, custom wallpapers using just a few words. It brings together color, mood, and creativity
