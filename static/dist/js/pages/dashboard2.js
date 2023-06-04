






const interest_chart=(data,labels)=>{
 var salesChartCanvas = $('#salesChart').get(0).getContext('2d');

  var salesChartData = {
    labels: labels,
    datasets: [
      {
        label: 'Test Intrest Chart',
        backgroundColor: '#d0a7ff',
        borderColor: 'rgba(60,141,188,0.8)',
        pointRadius: false,
        pointColor: '#3b8bba',
        pointStrokeColor: 'rgba(60,141,188,1)',
        pointHighlightFill: '#fff',
        pointHighlightStroke: 'rgba(60,141,188,1)',
        data: data
      }
    ]
  };

  var salesChartOptions = {
    maintainAspectRatio: false,
    responsive: true,
    legend: {
      display: false
    },
    scales: {
      xAxes: [{
        gridLines: {
          display: false
        }
      }],
      yAxes: [{
        gridLines: {
          display: false
        }
      }]
    }
  };
    var salesChart = new Chart(salesChartCanvas, {
    type: 'line',
    data: salesChartData,
    options: salesChartOptions
  }
  );
};


const getChartData=()=>{

    fetch('/plans/investment_per_plan_chart')
        .then((res)=>res.json())
        .then(
            (results)=>
            {
            console.log('results',results.users_data);
            const category_data=results.users_data;
            const [labels,data]=[
                Object.keys(category_data),
                Object.values(category_data)
            ];
            interest_chart(data,labels);



        });
};






const plan_chart=(data,labels,colors)=>{
     var pieChartCanvas = $('#pieChart').get(0).getContext('2d');
  var pieData = {
    labels: labels,
    datasets: [
      {
        data: data,
        backgroundColor: colors
      }
    ]
  }
  var pieOptions = {
    legend: {
      display: false
    }
  }

  var pieChart = new Chart(pieChartCanvas, {
    type: 'doughnut',
    data: pieData,
    options: pieOptions
  });

};


const getChartData2=()=>{

    fetch('/plans/active_running_plans')
        .then((res)=>res.json())
        .then(
            (results)=>
            {
            console.log('results',results.users_data);
            const category_data=results.users_data;
            const [labels,data]=[
                Object.keys(category_data),
                Object.values(category_data)
            ];
                var colors=[]
                for (var i = 0; i < labels.length; i++) {
                    console.log('line no 124',labels[i]);
                    var color;
                    switch (labels[i]) {

                        case 'BEGINNER':

                            color = "#56fffa";
                            break;
                        case 'INTERMEDIATE':
                            color = "#56b2ff";
                            break;
                        case 'ADVANCE':
                            color = "#7256ff";
                            break;
                        case 'MASTER':
                            color = "#c656ff";
                            break;

                    }
                    colors[i] = color;
                }
            plan_chart(data,labels,colors);



        });
};
document.onload=getChartData();
document.onload=getChartData2();


