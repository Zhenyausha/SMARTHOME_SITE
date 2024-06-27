function saveSettings() {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Пожалуйста, сначала ВОЙДИТЕ в систему');
        return;
    }

    const curtain_time = document.getElementById('curtain_time').value;
    const watering_time = document.getElementById('watering_time').value;

    fetch('/api/user_settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            jwt: token,
            curtain_time: curtain_time,
            watering_time: watering_time
        })
    }).then(response => {
        if (response.ok) {
            alert('Настройки сохранены');
        } else {
            alert('Не удалось сохранить настройки');
        }
    });
}

function getTemperature() {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Пожалуйста, сначала ВОЙДИТЕ в систему');
        return;
    }

    const decodedToken = jwt_decode(token);
    const username = decodedToken.username;

    fetch(`/api/user_settings?username=${username}`)
        .then(response => response.json())
        .then(data => {
            if (data.temperature) {
                document.getElementById('temperature_display').textContent = `Температура: ${data.temperature} °C`;
            }
            if (data.humidity) {
                document.getElementById('humidity_display').textContent = `Влажность: ${data.humidity} %`;
            }
        });
}

function controlDevice(endpoint) {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Пожалуйста, сначала ВОЙДИТЕ в систему');
        return;
    }

    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.ok) {
            alert('Устройство управляется успешно');
        } else {
            alert('Не удалось управлять устройством');
        }
    });
}

window.onload = getTemperature;
