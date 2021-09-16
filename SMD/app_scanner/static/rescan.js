let r;

function startft() {
    r = setInterval(fast, 10000)
}

function stopft() {
    console.log('stop')
    clearInterval(r)
}

function fast() {
    console.log('click')
    $.ajax({
        url: "",
        type: 'POST',
        data: {
            action: 'fast',
        },
        success: function(data) {
            console.log('fast')
            $('.emptyMe').load(' .emptyMe > * ')
        },
    })
}

function globals() {
    console.log('click2')
    $.ajax({
        url: "",
        method: 'POST',
        data: {
            action: 'long',
        },
        success: function(data) {
            console.log('global')
            $('.emptyMe').load(' .emptyMe > * ')
        },
    })
}

$(document).ready(function() {
    $('#button1').click(function() {
        console.log('btn1')
        startft()
    })
    $('#button2').click(function() {
        console.log('btn2')
        stopft()
        globals()
    })
    $('#button3').click(function() {
        console.log('btn3')
        stopft()
    })
})