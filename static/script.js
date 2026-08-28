let barChart, lineChart, historyChart, futureChart;

// 🔥 COUNT ANIMATION
function animateValue(id, start, end, duration = 800) {
    let element = document.getElementById(id);
    let range = end - start;
    let startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        let progress = timestamp - startTime;
        let value = Math.min(start + (range * progress / duration), end);
        element.innerText = value.toFixed(2);
        if (progress < duration) {
            requestAnimationFrame(step);
        }
    }
    requestAnimationFrame(step);
}

document.getElementById("predictForm").addEventListener("submit", async function(e) {

    e.preventDefault();

    let voltage = document.getElementById("voltage").value;
    let intensity = document.getElementById("intensity").value;

    let loading = document.getElementById("loading");
    loading.style.display = "block";

    try {

        let res = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ voltage, intensity })
        });

        let data = await res.json();

        loading.style.display = "none";

        if (data.error) {
            alert(data.error);
            return;
        }

        // ✨ ANIMATED VALUES
        animateValue("power", 0, data.prediction);
        animateValue("bill", 0, data.bill);
        animateValue("carbon", 0, data.carbon);

        document.getElementById("bestModel").innerText = data.best_model;
        document.getElementById("tip").innerText = data.tip;
        document.getElementById("anomaly").innerText = data.anomaly;

        // Destroy charts
        if (barChart) barChart.destroy();
        if (lineChart) lineChart.destroy();
        if (historyChart) historyChart.destroy();
        if (futureChart) futureChart.destroy();

        // 🔥 BAR CHART (ANIMATED)
        barChart = new Chart(document.getElementById("barChart"), {
            type: "bar",
            data: {
                labels: ["Power", "Bill"],
                datasets: [{
                    data: [data.prediction, data.bill],
                    backgroundColor: ["#22c55e", "#f59e0b"]
                }]
            },
            options: {
                animation: { duration: 1200 }
            }
        });

        // 🔥 TREND CHART
        lineChart = new Chart(document.getElementById("lineChart"), {
            type: "line",
            data: {
                labels: ["T1","T2","T3","T4","T5"],
                datasets: [{
                    data: [
                        data.prediction*0.8,
                        data.prediction*0.9,
                        data.prediction,
                        data.prediction*1.1,
                        data.prediction*1.05
                    ],
                    borderColor:"#38bdf8",
                    tension:0.4
                }]
            }
        });

        // HISTORY
        let histRes = await fetch("/api/history");
        let histData = await histRes.json();

        historyChart = new Chart(document.getElementById("historyChart"), {
            type: "line",
            data: {
                labels: histData.map((_,i)=>i+1),
                datasets: [{
                    data: histData,
                    borderColor:"#f43f5e"
                }]
            }
        });

        // FUTURE
        futureChart = new Chart(document.getElementById("futureChart"), {
            type: "line",
            data: {
                labels:["F1","F2","F3","F4","F5"],
                datasets:[{
                    data:data.future,
                    borderColor:"#22c55e"
                }]
            }
        });

    } catch (err) {
        loading.style.display = "none";
        alert("Something went wrong!");
    }

});