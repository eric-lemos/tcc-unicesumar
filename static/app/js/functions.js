$(document).ready(function() {
    const alert_errors = $('#alert-errors').detach()
    // Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    // Chart.defaults.global.defaultFontColor = '#858796';

    /* DATA TABLE */
    $('#calendar').DataTable({    
        language: {
            url:"/static/app/vendor/datatables/pt_BR.json"
        }, order: [[5, 'asc']]
    });

    $('#history').DataTable({    
        language: {
            url:"/static/app/vendor/datatables/pt_BR.json"
        }, order: [[4, 'desc']]
    });

    $('#dataTable').DataTable({    
        language: {
            url:"/static/app/vendor/datatables/pt_BR.json"
        }, order: [[1, 'asc']]
    });

    /* AUXILIAR GET AJAX FUNCTION */
    function displayItem(reference, element, value) {
        $(reference).find(element).val(value)
    }

    /* POST AJAX FUNCTION */
    function postItem(reference, endpoint) {
        $(reference).on('submit', function(event) {
            $('#addModalAlerts').html('');
            event.preventDefault();
            
            $.ajax({
                url: endpoint,
                method: "POST",
                data: $(this).serialize(),
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
                success: function(response) {
                    if (response.errors) {
                        const newline = alert_errors.clone()
                        response.errors.forEach(error => {
                            newline.find('#alert-message').append(
                                `<li>${error}</li>`
                            )
                        });
                        $('#addModalAlerts').append(newline)

                    } else {
                        window.location.reload()
                    }

                },
                error: function(xhr, status, error) {console.log(error)}
            });
        });
    }

    /* EDIT AJAX FUNCTION */
    function editItem(reference, endpoint, pk_reference) {
        $(reference).on('submit', function(event) {
            $('#modalAlerts').html('')
            event.preventDefault();
            const pk = $(pk_reference).val();

            $.ajax({
                url: `${endpoint}/${pk}`,
                method: "POST",
                data: $(this).serialize(),
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
                success: function(response) {
                    if (response.errors) {
                        const newline = alert_errors.clone()
                        response.errors.forEach(error => {
                            newline.find('#alert-message').append(
                                `<li>${error}</li>`
                            )
                        });
                        $('#editModalAlerts').append(newline)

                    } else {
                        window.location.reload()
                    }

                },
                error: function(xhr, status, error) {console.log(error)}
            });
        });
    }

    /* DEL AJAX FUNCTION */
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

    function delItem(reference, endpoint) {
        const csrftoken = getCookie('csrftoken');

        $(reference).on('click', function(event) {
            event.preventDefault();
            const pk = $(this).attr('data-pk')

            $.ajax({
                url: `${endpoint}/${pk}`,
                method: "POST",
                data: $(this).serialize(),
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                success: function(response) {
                    if (response.was_deleted) {
                        window.location.reload()
                    }
                },
                error: function(xhr, status, error) {console.log(error)}
            });
        });
    }

    /* MANAGERS */
    function getManagers(reference, endpoint) {
        $(reference).on('click', function(event) {
            const pk = $(this).attr('data-pk')
            $.ajax({
                url: `${endpoint}/${pk}`,
                method: "GET",
                success: function(response) {
                    displayItem('#editManager', '#manager_id', response.manager.id)
                    displayItem('#editManager', '#first_name', response.manager.first_name)
                    displayItem('#editManager', '#last_name', response.manager.last_name)
                    displayItem('#editManager', '#genrer', response.manager.genrer)
                    displayItem('#editManager', '#email', response.manager.email)
                    displayItem('#editManager', '#cpf', response.manager.cpf)
                },
                error: function(xhr, status, error) { console.log(error) }
            })
        })
    }
    
    delItem('.del-manager', 'managers/del')
    postItem('#add_manager', 'managers/add')
    getManagers('.edit-manager', 'managers/get')
    editItem('#edit_manager', 'managers/edit', '#manager_id')

    /* DOCTORS */
    function getDoctors(reference, endpoint) {
        $(reference).on('click', function(event) {
            const pk = $(this).attr('data-pk')
            $.ajax({
                url: `${endpoint}/${pk}`,
                method: "GET",
                success: function(response) {
                    console.log(response)
                    displayItem('#editDoctor', '#doctor_id', response.doctor.id)
                    displayItem('#editDoctor', '#first_name', response.doctor.first_name)
                    displayItem('#editDoctor', '#last_name', response.doctor.last_name)
                    displayItem('#editDoctor', '#genrer', response.doctor.genrer)
                    displayItem('#editDoctor', '#email', response.doctor.email)
                    displayItem('#editDoctor', '#cpf', response.doctor.cpf)
                    displayItem('#editDoctor', '#crm', response.doctor.crm)
                    displayItem('#editDoctor', '#crm_state', response.doctor.crm_state)
                    displayItem('#editDoctor', '#specialization', response.doctor.specialization)
                },
                error: function(xhr, status, error) { console.log(error) }
            })
        })
    }

    delItem('.del-doctor', 'doctors/del')
    postItem('#add_doctor', 'doctors/add')
    getDoctors('.edit-doctor', 'doctors/get')
    editItem('#edit_doctor', 'doctors/edit', '#doctor_id')

    /* PATIENTS */
    function getPatients(reference, endpoint) {
        $(reference).on('click', function(event) {
            const pk = $(this).attr('data-pk')
            $.ajax({
                url: `${endpoint}/${pk}`,
                method: "GET",
                success: function(response) {
                    displayItem('#editPatient', '#patient_id', response.patient.id)
                    displayItem('#editPatient', '#first_name', response.patient.first_name)
                    displayItem('#editPatient', '#last_name', response.patient.last_name)
                    displayItem('#editPatient', '#genrer', response.patient.genrer)
                    displayItem('#editPatient', '#email', response.patient.email)
                    displayItem('#editPatient', '#cpf', response.patient.cpf)
                },
                error: function(xhr, status, error) { console.log(error) }
            })
        })
    }
    
    delItem('.del-patient', 'patients/del')
    postItem('#add_patient', 'patients/add')
    getPatients('.edit-patient', 'patients/get')
    editItem('#edit_patient', 'patients/edit', '#patient_id')

    /* CALENDAR */
    /* CHANGE DOCTORS SPECIALIZATIONS IN CALENDAR SELECT ADD/EDIT MODAL */
    $('#specialization_select').on('change', function() { 
        var selectedValue = $(this).val();
        $('#doctor_select option').each(function() { 
            if (selectedValue === "" || $(this).data('specialization') === selectedValue) {
                $(this).show();
            } else { 
                $(this).hide(); 
            } 
        });
        $('#doctor_select').removeAttr('disabled')
        $('#doctor_select').val($('#doctor_select').find('option:visible').first().val())

    });

    $('#specialization_select_edit').on('change', function() { 
        var selectedValue = $(this).val();
        $('#doctor_select_edit option').each(function() { 
            if (selectedValue === "" || $(this).data('specialization') === selectedValue) {
                $(this).show();
            } else { 
                $(this).hide(); 
            } 
        });
        $('#doctor_select_edit').removeAttr('disabled')
        $('#doctor_select_edit').val($('#doctor_select_edit').find('option:visible').first().val())
    });

    function convertDatetime(datetimeString) {
        var localDateTime = moment.tz(datetimeString, 'America/Sao_Paulo').format('YYYY-MM-DDTHH:mm');
        return localDateTime;
    }

    function getCalendar(reference, endpoint) {
        $(reference).on('click', function(event) {
            const pk = $(this).attr('data-pk')
            $.ajax({
                url: `${endpoint}/${pk}`,
                method: "GET",
                success: function(response) {
                    
                    console.log(response)

                    $('#doctor_select_edit option').each(function() { 
                        if (response.appointments.specialization === "" || $(this).data('specialization') === response.appointments.specialization) {
                            $(this).show();
                        } else { 
                            $(this).hide(); 
                        } 
                    });

                    $('#doctor_select_edit').removeAttr('disabled')
                    $('#doctor_select_edit').val($('#doctor_select_edit').find('option:visible').first().val())

                    displayItem('#editAppointment', '#appointment_id_edit', response.appointments.id)
                    displayItem('#editAppointment', '#patient_select_edit', response.appointments.patient)
                    displayItem('#editAppointment', '#specialization_select_edit', response.appointments.specialization)
                    displayItem('#editAppointment', '#doctor_select_edit', response.appointments.doctor)
                    displayItem('#editAppointment', '#begin_date_edit', convertDatetime(response.appointments.begin_date))
                    displayItem('#editAppointment', '#end_date_edit', convertDatetime(response.appointments.end_date))
                },
                error: function(xhr, status, error) { console.log(error) }
            })
        })
    }
    
    postItem('#add_appointment', 'calendar/add')
    getCalendar('.edit-appointment', 'calendar/get')
    editItem('#edit_appointment', 'calendar/edit', '#appointment_id_edit')

    // Bar Chart
    barChart__labels = barChart.map(item => item.month),
    barChart__data = barChart.map(item => item.total)
    barChart__data.push(0)
    
    var ctx = document.getElementById("myBarChart").getContext('2d');
    var myBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: barChart__labels,
            datasets: [{
                label: "",
                backgroundColor: "#4e73df",
                hoverBackgroundColor: "#2e59d9",
                borderColor: "#4e73df",
                data: barChart__data,
                maxBarThickness: 25
            }],
        },
        options: {
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0
                }
            },
            scales: {
                x: {
                    time: {
                        unit: 'month'
                    },
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 6
                    }
                },
                y: {
                    ticks: {
                        min: 0,
                        max: 10,
                        maxTicksLimit: 5,
                        padding: 10,
                    },
                    grid: {
                        display: false,
                        drawBorder: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: "rgba(0,0,0,0.8)",
                    bodyFontColor: "#858796",
                    borderColor: '#dddfeb',
                    borderWidth: 1,
                    xPadding: 15,
                    yPadding: 15,
                    displayColors: false,
                    caretPadding: 10,
                    callbacks: {
                        label: function(tooltipItem) {
                            return `${tooltipItem.raw} agendamento(s)`
                        }
                    }
                }
            }
        }
    });

    // Pie Chart
    var ctx = document.getElementById("myPieChart").getContext('2d');
    var myPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["Cancelado", "Ausente", "Pendente", "Agendado", "Concluído"],
            datasets: [{
                data: [
                    parseInt($('#canceledAppointments').html()),
                    parseInt($('#awayAppointments').html()),
                    parseInt($('#pendingAppointments').html()),
                    parseInt($('#confirmedAppointments').html()),
                    parseInt($('#doneAppointments').html()),
                ],
                backgroundColor: ['#e74a3b', '#f6c23e', '#36b9cc', '#4e73df', '#1cc88a'],
                hoverBackgroundColor: ['#be2617', '#dda20a', '#258391', '#224abe', '#13855c'],
                hoverBorderColor: "rgba(234, 236, 244, 1)"
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: { 
                tooltip: {
                    backgroundColor: "rgb(255,255,255)",
                    bodyColor: "#858796",
                    borderColor: '#dddfeb',
                    borderWidth: 1,
                    padding: 15,
                    displayColors: false,
                    caretPadding: 10
                },
                legend: {
                    display: false
                }
            },
            cutout: '80%'
        }
    });
    

});


