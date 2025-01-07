const url = "http://127.0.0.1:5555";

// Datos para el gráfico de uso de CPU
const cpuUsageData = {
  labels: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40', '10:45'],
  datasets: [{
    label: 'CPU Usage (%)',
    data: [],
    borderColor: '#4CAF50',
    backgroundColor: 'rgba(76, 175, 80, 0.1)',
    borderWidth: 2,
    tension: 0.4,
    pointRadius: 4,
    pointBackgroundColor: '#4CAF50',
    pointBorderColor: '#ffffff'
  }]
};

const cpuUsageConfig = {
  type: 'line',
  data: cpuUsageData,
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: false
      },
    },
    scales: {
      x: {
        grid: {
          color: '#3c3c4d'
        },
        ticks: {
          color: '#b0b0c3'
        }
      },
      y: {
        grid: {
          color: '#3c3c4d'
        },
        ticks: {
          color: '#b0b0c3'
        },
        beginAtZero: true,
        max: 100
      }
    }
  }
};


// Data for RAM Usage Chart
const ramUsageData = {
  labels: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40', '10:45'],
  datasets: [{
    label: 'RAM Usage (GB)',
    data: [],
    borderColor: '#4CAF50',
    backgroundColor: 'rgba(76, 175, 80, 0.1)',
    borderWidth: 2,
    tension: 0.4,
    pointRadius: 3
  }]
};

const ramUsageConfig = {
  type: 'line',
  data: ramUsageData,
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: false
      },
    },
    scales: {
      x: {
        grid: {
          color: '#3c3c4d'
        },
        ticks: {
          color: '#b0b0c3'
        }
      },
      y: {
        grid: {
          color: '#3c3c4d'
        },
        ticks: {
          color: '#b0b0c3'
        },
        beginAtZero: true,
        max: 100
      }
    }
  }
};

// Data for Network Activity Chart
const networkActivityData = {
  labels: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40', '10:45'],
  datasets: [
    {
      label: 'Upload (MB/s)',
      data: [],
      borderColor: '#FF9800',
      backgroundColor: 'rgba(255, 152, 0, 0.1)',
      borderWidth: 2,
      tension: 0.4,
      pointRadius: 3
    },
    {
      label: 'Download (MB/s)',
      data: [],
      borderColor: '#03A9F4',
      backgroundColor: 'rgba(3, 169, 244, 0.1)',
      borderWidth: 2,
      tension: 0.4,
      pointRadius: 3
    }
  ]
};

const networkActivityConfig = {
  type: 'line',
  data: networkActivityData,
  options: {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: '#b0b0c3'
        }
      },
    },
    scales: {
      x: {
        grid: {
          color: '#3c3c4d'
        },
        ticks: {
          color: '#b0b0c3'
        }
      },
      y: {
        grid: {
          color: '#3c3c4d'
        },
        ticks: {
          color: '#b0b0c3'
        },
        beginAtZero: true,
        max: 500
      }
    }
  }
};

// Initialize Charts
const cpuUsageChart = new Chart(
  document.getElementById('cpuUsageChart'),
  cpuUsageConfig
);

const ramUsageChart = new Chart(
  document.getElementById('ramUsageChart'),
  ramUsageConfig
);

const networkActivityChart = new Chart(
  document.getElementById('networkActivityChart'),
  networkActivityConfig
);

function fetchData() {
  fetch("/api/data/realtime", {
    method: "GET",
    credentials: "include",
  })
    .then(response => response.json())
    .then(data => {
      if (data.length === 0) {
        console.warn("No data received.");
        return;
      }

      // Extraer los datos necesarios para los gráficos
      const newLabels = data.map(item => item.created_at);
      const newDataCpu = data.map(item => item.cpu_usage);
      const newDataRam = data.map(item => item.ram_percentage);
      const newDataUpload = data.map(item => item.network_upload);
      const newDataDownload = data.map(item => item.network_download);
      const diskUsage = data[0]?.disk_usage || 0;
      const diskTotalAmount = data[0]?.disk_total || 1;

      const cpuAmount = document.getElementById("cpu-amount");
      const ramAmount = document.getElementById("ram-amount");
      const diskAmount = document.getElementById("disk-amount");

      cpuAmount.innerText = newDataCpu[newDataCpu.length-1]+"%";
      ramAmount.innerText = newDataRam[newDataRam.length-1]+"%";
      diskAmount.innerText =  ((diskUsage / diskTotalAmount) * 100).toFixed(2) + "%";

      cpuUsageChart.data.labels = newLabels;
      cpuUsageChart.data.datasets[0].data = newDataCpu;
      cpuUsageChart.update();

      ramUsageChart.data.labels = newLabels;
      ramUsageChart.data.datasets[0].data = newDataRam;
      ramUsageChart.update();

      const maxUpload = Math.max(...newDataUpload);
      const maxDownload = Math.max(...newDataDownload);

      networkActivityChart.data.labels = newLabels;
      networkActivityChart.data.datasets[0].data = newDataUpload;
      networkActivityChart.data.datasets[1].data = newDataDownload;
      networkActivityChart.options.scales.y.max = maxUpload+maxDownload;
      networkActivityChart.update();

      const diskBar = document.getElementById("disk-bar");
      const diskUsed = document.getElementById("disk-used");
      const diskTotal = document.getElementById("disk-total");

      diskBar.style.width = Math.round((diskUsage / diskTotalAmount) * 100) + "%";
      diskUsed.innerText = diskUsage + "GB";
      diskTotal.innerText = diskTotalAmount + "GB"
    })
    .catch(error => {
      console.error("Error fetching data:", error);
    });
}

fetchData();
setInterval(fetchData, 5000);