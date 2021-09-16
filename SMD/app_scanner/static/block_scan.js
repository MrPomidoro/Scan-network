$(document).ready(function() {
    $("body").on("click", ".re-order-filter", function() {
        $('.select-all-option').prop('checked', false);
        let action = $(this).attr('data-action'),
            list_elements = [];
        $('.item-option').each(function(index) {
            list_elements.push({
                name: $(this).val(),
                id: $(this).attr('data-id'),
            });
        });
        if (action == "asc") {
            list_elements = list_elements.sort((a, b) => {
                if (a.name < b.name) return -1
                return a.name > b.name ? 1 : 0
            });
        } else {
            list_elements = list_elements.sort((a, b) => {
                if (a.name < b.name) return -1
                return a.name > b.name ? 1 : 0
            }).reverse();
        }
        $('.container-elements ul').html('');
        for (let item = 0; item < list_elements.length; item++) {
            $('.container-elements ul').append(function() {
                let html = '';
                html = '<li><label><input data-id="' + (list_elements[item].id) + '" class="item-option" value="' + (list_elements[item].name) + '" type="checkbox">' + (list_elements[item].name) + '</label></li>';
                return html;
            });
        }
    });
    $("body").on("keyup", ".search-button", function() {
        let search_content = $('.search-button').val().trim().toLowerCase();
        if (search_content.length > 0) {
            $('.item-option').each(function(index) {
                let content = $(this).val().toLowerCase(),
                    element = $(this);
                element.parent('label').parent('li').hide();
                if (content.indexOf(search_content) >= 0) {
                    element.parent('label').parent('li').show();
                }
            });
        } else {
            $('.item-option').parent('label').parent('li').show();
        }
    });

    $("body").on("click", ".container-buttons .accept", function() {
        $('.dropdown-advanced .container-elements').removeClass('opened');
        $('.dropdown-advanced .container-buttons').removeClass('opened');
        $('.dropdown-advanced .container-elements').addClass('closed');
        $('.dropdown-advanced .container-buttons').addClass('closed');
        $('.options-selected span').html('(' + ($('.item-option:checked').length) + ') seleccionados');
        $('.search-button').val("");
        $('.item-option').parent('label').parent('li').show();

        // $.ajax({
        //     url: "",
        //     type: 'POST',
        //     data: {
        //         val: $('#data').serialize(),
        //         csrfmiddlewaretoken: csrf_token,
        //     },
        //     dataType: 'text',
        //     success: function(data) {
        //         // $('tbody').load(' tbody > * ')
        //         console.log(data)
        //     },
        // })
        let csrftoken = '{{ csrf_token }}'
        let checkboxes_value = [];
        let inputval = $(".text").val(); //getting value of input field
        $('.item-option').each(function() {
            //if($(this).is(":checked")) { 
            if (this.checked) {
                checkboxes_value.push($(this).val());
            }
        });
        checkboxes_value = checkboxes_value.toString();
        $.ajax({
            url: "",
            headers: { 'X-CSRFToken': csrftoken },
            method: "POST",
            data: { checkboxes_value: checkboxes_value, inputval: inputval },
            success: function(data) {
                $('.echo').html(data);
            }
        });
    });

    $("body").on("click", ".container-buttons .cancel", function() {
        $('.dropdown-advanced .container-elements').removeClass('opened');
        $('.dropdown-advanced .container-buttons').removeClass('opened');

        $('.dropdown-advanced .container-elements').addClass('closed');
        $('.dropdown-advanced .container-buttons').addClass('closed');
        $('.search-button').val("");
        $('.item-option').parent('label').parent('li').show();
    });

    $("body").on("change", ".select-all-option", function() {
        if ($(this).is(':checked')) {
            $('.item-option').prop('checked', true);
        } else {
            $('.item-option').prop('checked', false);
        }
    });
    $("body").on("click", ".dropdown-advanced-fire-action", function() {
        if ($('.dropdown-advanced .container-elements').hasClass('opened')) {
            $('.dropdown-advanced .container-elements').removeClass('opened');
            $('.dropdown-advanced .container-buttons').removeClass('opened');

            $('.dropdown-advanced .container-elements').addClass('closed');
            $('.dropdown-advanced .container-buttons').addClass('closed');
        } else {
            $('.dropdown-advanced .container-elements').addClass('opened');
            $('.dropdown-advanced .container-buttons').addClass('opened');

            $('.dropdown-advanced .container-elements').removeClass('closed');
            $('.dropdown-advanced .container-buttons').removeClass('closed');
        }

    });
});