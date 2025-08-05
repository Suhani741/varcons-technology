// DOM Elements
const form = document.getElementById('wallpaperForm');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const downloadBtn = document.getElementById('downloadBtn');
const resolutionSelect = form.querySelector('select[name="resolution"]');
const colorTempRange = form.querySelector('input[name="colorTemp"]');

// Color palette constants
const VIBGYOR_COLORS = {
    violet: '#8B00FF',
    indigo: '#4B0082',
    blue: '#0000FF',
    green: '#00FF00',
    yellow: '#FFFF00',
    orange: '#FFA500',
    red: '#FF0000'
};

// Initialize style previews (now handled by select dropdown)
const styleSelect = form.querySelector('select[name="style"]');
styleSelect.addEventListener('change', (e) => {
    const style = e.target.value;
    showStylePreview(style);
});

// Form submission handler
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading state
    previewImage.classList.add('loading');
    downloadBtn.classList.add('d-none');
    
    // Get form data
    const formData = new FormData(form);
    const data = {
        color: formData.get('color'),
        style: formData.get('style'),
        description: formData.get('description'),
        resolution: formData.get('resolution'),
        colorTemp: formData.get('colorTemp')
    };
    
    try {
        // Send request to API
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            // Start preview polling
            startPreviewPolling(result.jobId);
        } else {
            showError('Failed to generate wallpaper');
        }
    } catch (error) {
        showError('Error generating wallpaper');
    }
});

// Preview polling function
let previewInterval;
async function startPreviewPolling(jobId) {
    previewInterval = setInterval(async () => {
        try {
            const response = await fetch(`/preview/${jobId}`);
            const data = await response.json();
            
            if (data.status === 'success' && data.previewUrl) {
                clearInterval(previewInterval);
                previewImage.classList.remove('loading');
                previewImage.style.backgroundImage = `url(${data.previewUrl})`;
                downloadBtn.classList.remove('d-none');
                downloadBtn.onclick = () => downloadWallpaper(data.previewUrl);
            }
        } catch (error) {
            clearInterval(previewInterval);
            showError('Error loading preview');
        }
    }, 1000);
}

// Download wallpaper function
function downloadWallpaper(url) {
    const link = document.createElement('a');
    link.href = url;
    link.download = 'luminous-wallpaper.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Error handling
function showError(message) {
    previewContainer.innerHTML = `
        <div class="error">
            <i class="fas fa-exclamation-circle"></i>
            ${message}
        </div>
    `;
}

// Add color preview to select options
const colorSelect = form.querySelector('select[name="color"]');
Array.from(colorSelect.options).forEach(option => {
    if (VIBGYOR_COLORS[option.value]) {
        option.style.backgroundColor = VIBGYOR_COLORS[option.value];
        option.style.color = '#fff';
    }
});

// Show style preview
function showStylePreview(style) {
    const preview = document.querySelector(`.${style}-preview`);
    if (preview) {
        preview.classList.add('active');
        setTimeout(() => preview.classList.remove('active'), 200);
    }
}

// Color temperature change handler
colorTempRange.addEventListener('input', (e) => {
    const temp = e.target.value;
    document.documentElement.style.setProperty('--color-temp', `${temp}K`);
});

// Initialize color temperature
const currentTemp = colorTempRange.value;
document.documentElement.style.setProperty('--color-temp', `${currentTemp}K`);
