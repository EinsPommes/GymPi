// Dashboard-Funktionalität
let heartRateChart = null;

// Lade alle Geräte
async function loadDevices() {
    try {
        const response = await fetch('/api/devices');
        const devices = await response.json();
        displayDevices(devices);
    } catch (error) {
        console.error('Fehler beim Laden der Geräte:', error);
    }
}

// Zeige Geräte an
function displayDevices(devices) {
    const container = document.getElementById('devices-container');
    container.innerHTML = '';

    devices.forEach(device => {
        const deviceCard = createDeviceCard(device);
        container.appendChild(deviceCard);
    });
}

// Erstelle Gerätekarte
function createDeviceCard(device) {
    const col = document.createElement('div');
    col.className = 'col-md-4';
    
    col.innerHTML = `
        <div class="card device-card">
            <div class="card-body">
                <h5 class="card-title">Gerät ${device.device_id}</h5>
                <div class="row">
                    <div class="col-4">
                        <div class="stat-card">
                            <h6>Workouts</h6>
                            <p>${device.stats.total_workouts}</p>
                        </div>
                    </div>
                    <div class="col-4">
                        <div class="stat-card">
                            <h6>Übungen</h6>
                            <p>${device.stats.total_exercises}</p>
                        </div>
                    </div>
                    <div class="col-4">
                        <div class="stat-card">
                            <h6>Ø Puls</h6>
                            <p>${device.stats.average_heart_rate} BPM</p>
                        </div>
                    </div>
                </div>
                <button class="btn btn-primary mt-3" onclick="showDeviceDetails('${device.device_id}')">
                    Details
                </button>
            </div>
        </div>
    `;
    
    return col;
}

// Zeige Gerätedetails
async function showDeviceDetails(deviceId) {
    const modal = new bootstrap.Modal(document.getElementById('deviceModal'));
    
    try {
        // Lade Workout-Historie
        const historyResponse = await fetch(`/workout/history/${deviceId}`);
        const history = await historyResponse.json();
        
        // Zeige Workout-Historie
        displayWorkoutHistory(history);
        
        // Erstelle Herzfrequenz-Chart
        createHeartRateChart(history);
        
        modal.show();
    } catch (error) {
        console.error('Fehler beim Laden der Details:', error);
    }
}

// Zeige Workout-Historie
function displayWorkoutHistory(history) {
    const container = document.getElementById('workoutHistory');
    container.innerHTML = '<h4>Trainingshistorie</h4>';
    
    const table = document.createElement('table');
    table.className = 'table';
    table.innerHTML = `
        <thead>
            <tr>
                <th>Datum</th>
                <th>Workout</th>
                <th>Übungen</th>
                <th>Ø Herzfrequenz</th>
            </tr>
        </thead>
        <tbody>
            ${history.map(workout => `
                <tr>
                    <td>${new Date(workout.timestamp).toLocaleDateString()}</td>
                    <td>${workout.workout_name}</td>
                    <td>${workout.completed_exercises}</td>
                    <td>${calculateAverageHeartRate(workout.heart_rate_data)} BPM</td>
                </tr>
            `).join('')}
        </tbody>
    `;
    
    container.appendChild(table);
}

// Erstelle Herzfrequenz-Chart
function createHeartRateChart(history) {
    if (heartRateChart) {
        heartRateChart.destroy();
    }
    
    const ctx = document.getElementById('heartRateChart').getContext('2d');
    const latestWorkout = history[0];
    
    if (!latestWorkout) return;
    
    const heartRateData = latestWorkout.heart_rate_data;
    const labels = heartRateData.map((_, index) => index);
    const data = heartRateData.map(d => d.value);
    
    heartRateChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Herzfrequenz',
                data: data,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    suggestedMax: 200
                }
            }
        }
    });
}

// Berechne durchschnittliche Herzfrequenz
function calculateAverageHeartRate(heartRateData) {
    if (!heartRateData || heartRateData.length === 0) return 0;
    const sum = heartRateData.reduce((acc, curr) => acc + curr.value, 0);
    return Math.round(sum / heartRateData.length);
}

// Initialisierung
document.addEventListener('DOMContentLoaded', () => {
    loadDevices();
    // Aktualisiere alle 30 Sekunden
    setInterval(loadDevices, 30000);
});
