// Extract query parameters from URL
const params = new URLSearchParams(window.location.search);
const anime = params.get('anime');
const title = params.get('title');
const rating = params.get('rating');
const seasons = params.get('seasons');

// Update the page content dynamically
document.getElementById('anime-title').textContent = title || 'Anime';
document.getElementById('anime-rating').textContent = `⭐ Rating: ${rating || 'N/A'}`;
document.getElementById('anime-seasons').textContent = `📺 Seasons: ${seasons || 'N/A'}`;

// Set the video source dynamical
if (anime) {
  document.getElementById('anime-video').querySelector('source').src = `${anime}.mp4`;
  document.getElementById('anime-video').load(); // Reload the video with the new source
}

// Generate episode buttons
const episodesContainer = document.getElementById('episodes');
const numEpisodes = 12; // Adjust this based on the number of episodes for each season
for (let i = 1; i <= numEpisodes; i++) {
  const button = document.createElement('button');
  button.classList.add('episode-btn');
  button.textContent = `Ep ${i}`;
  button.addEventListener('click', () => playEpisode(i));
  episodesContainer.appendChild(button);
}

// Function to handle episode button click
function playEpisode(episode) {
  const videoElement = document.getElementById('anime-video');
  const source = videoElement.querySelector('source');
  source.src = `${anime}_episode${episode}.mp4`; // Assuming the episode files are named accordingly
  videoElement.load(); // Reload the video with the new source
  highlightWatched(episode); // Mark the episode as watched
}

// Mark episode as watched
function highlightWatched(episode) {
  const episodeButtons = document.querySelectorAll('.episode-btn');
  episodeButtons.forEach(button => {
    if (button.textContent === `Ep ${episode}`) {
      button.classList.add('watched');
    }
  });
}
