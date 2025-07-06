// Explore Nearby JavaScript

let map;
let userMarker;
let landmarkMarkers = [];
let currentPosition = null;
let allLandmarks = []; // Store all landmarks for filtering
let filteredLandmarks = []; // Store currently filtered landmarks

// Landmark type configuration with colors and icons
const landmarkTypes = {
    'Tourist Attraction': {
        color: '#3b82f6', // Blue
        icon: 'bi-star-fill',
        bgColor: '#dbeafe'
    },
    'Monument': {
        color: '#8b5cf6', // Purple
        icon: 'bi-building',
        bgColor: '#ede9fe'
    },
    'Museum': {
        color: '#06b6d4', // Cyan
        icon: 'bi-collection',
        bgColor: '#cffafe'
    },
    'Park': {
        color: '#10b981', // Green
        icon: 'bi-tree-fill',
        bgColor: '#d1fae5'
    },
    'Restaurant': {
        color: '#f59e0b', // Amber
        icon: 'bi-cup-hot-fill',
        bgColor: '#fef3c7'
    },
    'Shopping Mall': {
        color: '#ef4444', // Red
        icon: 'bi-shop',
        bgColor: '#fee2e2'
    },
    'Landmark': {
        color: '#6366f1', // Indigo (default)
        icon: 'bi-geo-alt-fill',
        bgColor: '#e0e7ff'
    }
};

// Initialize the explore page
document.addEventListener('DOMContentLoaded', function() {
    initMap();
    initEventListeners();
    getCurrentLocation();
    loadSavedLocations();
});

// Global variable to store saved location IDs
let savedLocationIds = [];

// Load saved locations to check which ones are already saved
async function loadSavedLocations() {
    try {
        const response = await fetch('/get-saved-locations/');
        const result = await response.json();
        
        if (result.success) {
            // Convert all place IDs to strings for consistent comparison
            savedLocationIds = result.saved_place_ids.map(id => id.toString());
            console.log('Loaded saved location IDs:', savedLocationIds);
        }
    } catch (error) {
        console.error('Error loading saved locations:', error);
    }
}

// Initialize the map
function initMap() {
    // Initialize map centered on a default location (can be anywhere)
    map = L.map('map').setView([40.7128, -74.0060], 13); // Default to NYC
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18
    }).addTo(map);
    
    // Custom marker icons
    const userIcon = L.divIcon({
        className: 'user-marker',
        html: '<i class="bi bi-person-fill" style="color: white; font-size: 12px; line-height: 20px; text-align: center; width: 100%;"></i>',
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    });
    
    // Store icons globally
    window.userIcon = userIcon;
}

// Initialize event listeners
function initEventListeners() {
    const getLocationBtn = document.getElementById('getLocationBtn');
    const refreshBtn = document.getElementById('refreshBtn');
    const landmarkFilter = document.getElementById('landmarkFilter');
    
    if (getLocationBtn) {
        getLocationBtn.addEventListener('click', getCurrentLocation);
    }
    
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshLandmarks);
    }
    
    if (landmarkFilter) {
        landmarkFilter.addEventListener('change', filterLandmarks);
    }
}

// Get current location
function getCurrentLocation() {
    updateLocationInfo('Getting your location...');
    showLoadingState();
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const { latitude, longitude } = position.coords;
                currentPosition = { lat: latitude, lng: longitude };
                
                // Update map to user's location
                map.setView([latitude, longitude], 15);
                
                // Add or update user marker
                if (userMarker) {
                    userMarker.setLatLng([latitude, longitude]);
                } else {
                    userMarker = L.marker([latitude, longitude], { icon: window.userIcon })
                        .addTo(map)
                        .bindPopup('Your Location')
                        .openPopup();
                }
                
                // Get reverse geocoding for location name
                getLocationName(latitude, longitude);
                
                // Fetch nearby landmarks
                fetchNearbyLandmarks(latitude, longitude);
            },
            function(error) {
                console.error('Geolocation error:', error);
                handleLocationError(error);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 300000 // 5 minutes
            }
        );
    } else {
        handleLocationError({ code: 0, message: 'Geolocation is not supported by this browser.' });
    }
}

// Get location name from coordinates
async function getLocationName(lat, lng) {
    try {
        const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=10`);
        const data = await response.json();
        
        if (data.display_name) {
            const locationName = data.display_name.split(',')[0]; // Get first part of address
            updateLocationInfo(`📍 ${locationName}`);
        } else {
            updateLocationInfo(`📍 ${lat.toFixed(4)}, ${lng.toFixed(4)}`);
        }
    } catch (error) {
        console.error('Error getting location name:', error);
        updateLocationInfo(`📍 ${lat.toFixed(4)}, ${lng.toFixed(4)}`);
    }
}

// Fetch nearby landmarks using OpenStreetMap Overpass API
async function fetchNearbyLandmarks(lat, lng) {
    try {
        showLoadingState();
        
        // Define search radius (in meters)
        const radius = 2000; // 2km
        
        // Overpass query for tourist attractions, monuments, museums, etc.
        const query = `
            [out:json][timeout:25];
            (
                node["tourism"="attraction"](around:${radius},${lat},${lng});
                node["historic"="monument"](around:${radius},${lat},${lng});
                node["tourism"="museum"](around:${radius},${lat},${lng});
                node["leisure"="park"](around:${radius},${lat},${lng});
                node["amenity"="restaurant"](around:${radius},${lat},${lng});
                node["shop"="mall"](around:${radius},${lat},${lng});
                way["tourism"="attraction"](around:${radius},${lat},${lng});
                way["historic"="monument"](around:${radius},${lat},${lng});
                way["tourism"="museum"](around:${radius},${lat},${lng});
                way["leisure"="park"](around:${radius},${lat},${lng});
                way["amenity"="restaurant"](around:${radius},${lat},${lng});
                way["shop"="mall"](around:${radius},${lat},${lng});
            );
            out center;
        `;
        
        const response = await fetch('https://overpass-api.de/api/interpreter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `data=${encodeURIComponent(query)}`
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch landmarks');
        }
        
        const data = await response.json();
        await processLandmarks(data.elements, lat, lng);
        
    } catch (error) {
        console.error('Error fetching landmarks:', error);
        showErrorState('Failed to load landmarks. Please try again.');
    }
}

// Process landmarks data
async function processLandmarks(elements, userLat, userLng) {
    // Clear existing markers
    clearLandmarkMarkers();
    
    const landmarks = [];
    
    // First pass: create landmarks with basic info
    for (const element of elements) {
        if (element.tags && element.tags.name) {
            let lat, lng;
            
            // Handle different element types
            if (element.type === 'node') {
                lat = element.lat;
                lng = element.lon;
            } else if (element.type === 'way' && element.center) {
                lat = element.center.lat;
                lng = element.center.lon;
            } else {
                continue; // Skip if we can't get coordinates
            }
            
            // Calculate distance
            const distance = calculateDistance(userLat, userLng, lat, lng);
            
            // Only include landmarks within 2km
            if (distance <= 2) {
                let description = getLandmarkDescription(element.tags);
                const wikipedia = getWikipediaLink(element.tags);
                
                // If we have Wikipedia info, try to fetch description and image
                let imageUrl = null;
                if (element.tags.wikipedia) {
                    const wikiTitle = element.tags.wikipedia.replace(/^en:/, '');
                    const wikiData = await fetchWikipediaData(wikiTitle);
                    if (wikiData.description && !element.tags.description) {
                        description = wikiData.description;
                    }
                    if (wikiData.imageUrl) {
                        imageUrl = wikiData.imageUrl;
                    }
                }
                
                // Check for image URL in OpenStreetMap tags
                if (!imageUrl && element.tags.image) {
                    imageUrl = element.tags.image;
                }
                if (!imageUrl && element.tags.photo) {
                    imageUrl = element.tags.photo;
                }
                if (!imageUrl && element.tags.website && element.tags.website.includes('flickr.com')) {
                    // Try to extract image from Flickr URLs
                    const flickrMatch = element.tags.website.match(/flickr\.com\/photos\/[^\/]+\/(\d+)/);
                    if (flickrMatch) {
                        imageUrl = `https://live.staticflickr.com/${flickrMatch[1]}/size_m.jpg`;
                    }
                }
                
                const landmark = {
                    id: element.id,
                    name: element.tags.name,
                    type: getLandmarkType(element.tags),
                    lat: lat,
                    lng: lng,
                    distance: distance,
                    description: description,
                    wikipedia: wikipedia,
                    imageUrl: imageUrl
                };
                
                landmarks.push(landmark);
            }
        }
    }
    
    // Sort by distance
    landmarks.sort((a, b) => a.distance - b.distance);
    
    // Store all landmarks for filtering
    allLandmarks = landmarks;
    filteredLandmarks = landmarks;
    
    // Display landmarks
    displayLandmarks(landmarks);
    addLandmarkMarkers(landmarks);
}

// Get landmark type from tags
function getLandmarkType(tags) {
    if (tags.tourism === 'attraction') return 'Tourist Attraction';
    if (tags.historic === 'monument') return 'Monument';
    if (tags.tourism === 'museum') return 'Museum';
    if (tags.leisure === 'park') return 'Park';
    if (tags.amenity === 'restaurant') return 'Restaurant';
    if (tags.shop === 'mall') return 'Shopping Mall';
    if (tags.amenity === 'cafe') return 'Restaurant';
    if (tags.amenity === 'bar') return 'Restaurant';
    if (tags.amenity === 'pub') return 'Restaurant';
    if (tags.historic === 'castle') return 'Monument';
    if (tags.historic === 'ruins') return 'Monument';
    if (tags.historic === 'church') return 'Monument';
    if (tags.amenity === 'theatre') return 'Tourist Attraction';
    if (tags.amenity === 'cinema') return 'Tourist Attraction';
    if (tags.leisure === 'sports_centre') return 'Tourist Attraction';
    if (tags.amenity === 'hospital') return 'Landmark';
    if (tags.amenity === 'school') return 'Landmark';
    if (tags.amenity === 'university') return 'Landmark';
    if (tags.amenity === 'bank') return 'Landmark';
    if (tags.amenity === 'post_office') return 'Landmark';
    if (tags.amenity === 'police') return 'Landmark';
    if (tags.amenity === 'fire_station') return 'Landmark';
    return 'Landmark';
}

// Get landmark description from tags
function getLandmarkDescription(tags) {
    if (tags.description) return tags.description;
    if (tags.tourism === 'attraction') return 'Popular tourist destination.';
    if (tags.historic === 'monument') return 'Historical monument of cultural significance.';
    return 'Interesting place to visit.';
}

// Get Wikipedia link from tags
function getWikipediaLink(tags) {
    if (tags.wikipedia) {
        // Extract the page title from the Wikipedia tag
        const wikiTitle = tags.wikipedia.replace(/^en:/, ''); // Remove language prefix if present
        return `https://en.wikipedia.org/wiki/${encodeURIComponent(wikiTitle)}`;
    }
    return null;
}

// Fetch Wikipedia description and image using Wikipedia API
async function fetchWikipediaData(wikiTitle) {
    try {
        const response = await fetch(`https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(wikiTitle)}`);
        const data = await response.json();
        
        let description = null;
        let imageUrl = null;
        
        if (data.extract) {
            // Limit description to 150 characters and add ellipsis if longer
            description = data.extract.length > 150 
                ? data.extract.substring(0, 150) + '...' 
                : data.extract;
        }
        
        if (data.thumbnail && data.thumbnail.source) {
            imageUrl = data.thumbnail.source;
        }
        
        return { description, imageUrl };
    } catch (error) {
        console.error('Error fetching Wikipedia data:', error);
        return { description: null, imageUrl: null };
    }
}

// Calculate distance between two points
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth's radius in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

// Display landmarks in the panel
function displayLandmarks(landmarks) {
    const landmarksList = document.getElementById('landmarksList');
    
    // Update count in header
    const filterValue = document.getElementById('landmarkFilter').value;
    const totalCount = allLandmarks.length;
    const filteredCount = landmarks.length;
    
    if (filterValue === 'all') {
        document.querySelector('.panel-header h4').innerHTML = `<i class="bi bi-geo-alt"></i> Nearby Landmarks <span class="badge bg-secondary ms-2">${totalCount}</span>`;
    } else {
        document.querySelector('.panel-header h4').innerHTML = `<i class="bi bi-geo-alt"></i> Nearby Landmarks <span class="badge bg-secondary ms-2">${filteredCount}/${totalCount}</span>`;
    }
    
    if (landmarks.length === 0) {
        landmarksList.innerHTML = `
            <div class="error-state">
                <i class="bi bi-exclamation-triangle"></i>
                <p>No landmarks found for this filter.</p>
                <small>Try selecting a different landmark type or moving to a different location.</small>
            </div>
        `;
        return;
    }
    
    landmarksList.innerHTML = landmarks.map(landmark => {
        const typeConfig = landmarkTypes[landmark.type] || landmarkTypes['Landmark'];
        const wikiLink = landmark.wikipedia ? `
            <div class="landmark-wiki">
                <a href="${landmark.wikipedia}" target="_blank" class="wiki-link">
                    <i class="bi bi-wikipedia"></i> Read on Wikipedia
                </a>
            </div>
        ` : '';
        
        const backgroundStyle = landmark.imageUrl ? 
            `background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8)), url('${landmark.imageUrl}'); background-size: cover; background-position: center;` : '';
        
        // Check if this location is already saved
        const isSaved = savedLocationIds.includes(landmark.id.toString());
        const buttonClass = isSaved ? 'btn-save-location saved' : 'btn-save-location';
        const buttonIcon = isSaved ? 'bi-bookmark-check' : 'bi-bookmark-plus';
        const buttonColor = isSaved ? '#10b981' : '#6366f1';
        const buttonTitle = isSaved ? 'Remove from travel plan' : 'Save to travel plan';
        
        return `
            <div class="landmark-item ${landmark.imageUrl ? 'landmark-with-image' : ''}" data-landmark-id="${landmark.id}" style="${backgroundStyle}">
                <div class="landmark-header">
                    <div class="landmark-icon" style="background-color: ${typeConfig.bgColor}; color: ${typeConfig.color};">
                        <i class="${typeConfig.icon}"></i>
                    </div>
                    <div class="landmark-info">
                        <div class="landmark-name">${landmark.name}</div>
                        <div class="landmark-type" style="color: ${typeConfig.color};">${landmark.type}</div>
                    </div>
                    <button class="${buttonClass}" onclick="saveLocation(event, ${JSON.stringify(landmark).replace(/"/g, '&quot;')})" title="${buttonTitle}" style="background-color: ${buttonColor}; color: white;">
                        <i class="bi ${buttonIcon}"></i>
                    </button>
                </div>
                <div class="landmark-distance">${landmark.distance.toFixed(1)} km away</div>
                <div class="landmark-description">${landmark.description}</div>
                ${wikiLink}
            </div>
        `;
    }).join('');
    
    // Add click listeners to landmark items
    document.querySelectorAll('.landmark-item').forEach(item => {
        item.addEventListener('click', function() {
            const landmarkId = this.dataset.landmarkId;
            const landmark = landmarks.find(l => l.id == landmarkId);
            if (landmark) {
                selectLandmark(landmark);
            }
        });
    });
    

}

// Add markers to map
function addLandmarkMarkers(landmarks) {
    landmarks.forEach(landmark => {
        const typeConfig = landmarkTypes[landmark.type] || landmarkTypes['Landmark'];
        
        // Create custom icon for this landmark type with specific background color
        const customIcon = L.divIcon({
            className: 'custom-marker',
            html: `<i class="${typeConfig.icon}" style="color: ${typeConfig.color}; font-size: 12px; line-height: 24px; text-align: center; width: 100%;"></i>`,
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        });
        
        const wikiLink = landmark.wikipedia ? `
            <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb;">
                <a href="${landmark.wikipedia}" target="_blank" style="color: #6366f1; text-decoration: none; font-size: 0.8em; display: flex; align-items: center; gap: 4px;">
                    <i class="bi bi-wikipedia" style="font-size: 0.9em;"></i> Wikipedia
                </a>
            </div>
        ` : '';
        
        const marker = L.marker([landmark.lat, landmark.lng], { icon: customIcon })
            .addTo(map)
            .bindPopup(`
                <div style="min-width: 200px;">
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <div style="background-color: ${typeConfig.bgColor}; color: ${typeConfig.color}; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 8px;">
                            <i class="${typeConfig.icon}" style="font-size: 12px;"></i>
                        </div>
                        <h6 style="margin: 0; color: ${typeConfig.color};">${landmark.name}</h6>
                    </div>
                    <p style="margin: 0 0 4px 0; font-size: 0.9em; color: ${typeConfig.color}; font-weight: 500;">${landmark.type}</p>
                    <p style="margin: 0; font-size: 0.8em; color: #a1a1aa;">${landmark.distance.toFixed(1)} km away</p>
                    ${wikiLink}
                </div>
            `);
        

        
        landmarkMarkers.push(marker);
    });
}

// Clear landmark markers
function clearLandmarkMarkers() {
    landmarkMarkers.forEach(marker => {
        map.removeLayer(marker);
    });
    landmarkMarkers = [];
}

// Select landmark
function selectLandmark(landmark) {
    // Remove previous selection
    document.querySelectorAll('.landmark-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    // Add selection to clicked item
    const selectedItem = document.querySelector(`[data-landmark-id="${landmark.id}"]`);
    if (selectedItem) {
        selectedItem.classList.add('selected');
    }
    
    // Center map on landmark
    map.setView([landmark.lat, landmark.lng], 16);
    
    // Open popup for the corresponding marker
    const marker = landmarkMarkers.find(m => {
        const pos = m.getLatLng();
        return pos.lat === landmark.lat && pos.lng === landmark.lng;
    });
    
    if (marker) {
        marker.openPopup();
    }
}

// Filter landmarks by type
function filterLandmarks() {
    const filterValue = document.getElementById('landmarkFilter').value;
    
    if (filterValue === 'all') {
        filteredLandmarks = allLandmarks;
    } else {
        filteredLandmarks = allLandmarks.filter(landmark => landmark.type === filterValue);
    }
    
    // Clear existing markers and display
    clearLandmarkMarkers();
    displayLandmarks(filteredLandmarks);
    addLandmarkMarkers(filteredLandmarks);
}

// Refresh landmarks
function refreshLandmarks() {
    if (currentPosition) {
        fetchNearbyLandmarks(currentPosition.lat, currentPosition.lng);
    } else {
        getCurrentLocation();
    }
}

// Update location info
function updateLocationInfo(text) {
    const locationInfo = document.getElementById('locationInfo');
    if (locationInfo) {
        locationInfo.textContent = text;
    }
}

// Show loading state
function showLoadingState() {
    const landmarksList = document.getElementById('landmarksList');
    landmarksList.innerHTML = `
        <div class="loading-placeholder">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-light mt-2">Finding landmarks near you...</p>
        </div>
    `;
}

// Show error state
function showErrorState(message) {
    const landmarksList = document.getElementById('landmarksList');
    landmarksList.innerHTML = `
        <div class="error-state">
            <i class="bi bi-exclamation-triangle"></i>
            <p>${message}</p>
        </div>
    `;
}

// Save location to travel plan
async function saveLocation(event, landmark) {
    event.stopPropagation(); // Prevent landmark selection
    
    const button = event.target.closest('.btn-save-location');
    const isSaved = button.classList.contains('saved');
    
    console.log('Save/Unsave clicked for landmark:', landmark.id, 'isSaved:', isSaved);
    console.log('Current savedLocationIds:', savedLocationIds);
    
    if (isSaved) {
        // Unsave location
        try {
            const response = await fetch(`/remove-saved-location-ajax/${landmark.id}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Change button back to unsaved state
                button.innerHTML = '<i class="bi bi-bookmark-plus"></i>';
                button.style.backgroundColor = '#6366f1';
                button.style.color = 'white';
                button.classList.remove('saved');
                button.title = 'Save to travel plan';
                
                // Remove from saved locations array
                const index = savedLocationIds.indexOf(landmark.id.toString());
                if (index > -1) {
                    savedLocationIds.splice(index, 1);
                }
            }
        } catch (error) {
            console.error('Error removing location:', error);
        }
    } else {
        // Save location
        try {
            const response = await fetch('/save-location/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    place_id: landmark.id,
                    name: landmark.name,
                    address: landmark.description || 'No address available',
                    latitude: landmark.lat,
                    longitude: landmark.lng,
                    types: [landmark.type],
                    rating: null,
                    user_ratings_total: null
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Change button to saved state
                button.innerHTML = '<i class="bi bi-bookmark-check"></i>';
                button.style.backgroundColor = '#10b981';
                button.style.color = 'white';
                button.classList.add('saved');
                button.title = 'Remove from travel plan';
                
                // Add to saved locations array
                if (!savedLocationIds.includes(landmark.id.toString())) {
                    savedLocationIds.push(landmark.id.toString());
                }
            }
        } catch (error) {
            console.error('Error saving location:', error);
        }
    }
}



// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Handle location error
function handleLocationError(error) {
    let message = 'Unable to get your location.';
    
    switch(error.code) {
        case 1:
            message = 'Location access denied. Please enable location services.';
            break;
        case 2:
            message = 'Location unavailable. Please try again.';
            break;
        case 3:
            message = 'Location request timed out. Please try again.';
            break;
    }
    
    updateLocationInfo('❌ Location unavailable');
    showErrorState(message);
} 