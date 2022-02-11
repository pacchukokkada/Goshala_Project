$(document).ready(function() {
	
	$.ajax(
		{
			type:"GET",
			url:"/income-chart/",
			success: function(data)
			{
				// Income/Expense Line Chart
				var lineChartData = {
					labels: data.labels,
					datasets: [{
						label: "income",
						backgroundColor: "rgba(0, 158, 251, 0.5)",
						data: data.income_data
					}, {
					label: "expense",
					backgroundColor: "rgba(255, 188, 53, 0.5)",
					fill: true,
					data: data.expense_data
					}]
				};
				
				var linectx = document.getElementById('linegraph').getContext('2d');
				window.myLine = new Chart(linectx, {
					type: 'line',
					data: lineChartData,
					options: {
						responsive: true,
						legend: {
							display: false,
						},
						tooltips: {
							mode: 'index',
							intersect: false,
						}
					}
				});

				//Milk Bar Chart
				var barChartData = {
					labels: data.labels,
					datasets: [{
						label: 'Milk Production',
						backgroundColor: 'rgba(255, 188, 53, 0.5)',
						borderColor: 'rgba(255, 188, 53, 1)',
						borderWidth: 1,
						data: data.milk_data
					}]
					// , {
					// 	label: 'Dataset 2',
					// 	backgroundColor: 'rgba(255, 188, 53, 0.5)',
					// 	borderColor: 'rgba(255, 188, 53, 1)',
					// 	borderWidth: 1,
					// 	data: [28, 48, 40, 19, 86, 27, 90]
					// }]
				};
				var ctx = document.getElementById('bargraph').getContext('2d');
				window.myBar = new Chart(ctx, {
					type: 'bar',
					data: barChartData,
					options: {
						responsive: true,
						legend: {
							display: false,
						}
					}
				});
			}
		}
	)
	
	
	// Bar Chart 2
	
    // barChart();
    
    // $(window).resize(function(){
    //     barChart();
    // });
    
    // function barChart(){
    //     $('.bar-chart').find('.item-progress').each(function(){
    //         var itemProgress = $(this),
    //         itemProgressWidth = $(this).parent().width() * ($(this).data('percent') / 100);
    //         itemProgress.css('width', itemProgressWidth);
    //     });
    // };
});