let r
$(document).ready(function() {
    $('.send').click(function() {
        r = setInterval(function() {
            $.ajax({
                url: "",
                type: 'GET',
                data: {
                    'name': 'top'
                },
                success: function(data) {
                    $('tbody').load(' tbody > * ')
                    console.log('fast')
                },
            })

        }, 3000)
    })
})