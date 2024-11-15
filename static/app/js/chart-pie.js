Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Cancelado", "Ausente", "Pendente", "Agendado", "Concluído"],
    datasets: [{
        data: [20, 20, 20, 20, 20],
        backgroundColor: ['#e74a3b', '#f6c23e', '#36b9cc', '#4e73df', '#1cc88a'],
        hoverBackgroundColor: ['#be2617', '#dda20a', '#258391', '#224abe', '#13855c'],
        hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
    },
    legend: {
        display: false
    },
    cutoutPercentage: 80,
  },
});
