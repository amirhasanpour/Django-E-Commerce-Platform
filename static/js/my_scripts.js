function showVal(x) {
    x = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    document.getElementById('sel_price').innerText = x;
}



function removeURLParameter(url, parameter) {
    var urlparts = url.split('?');
    if (urlparts.length >= 2) {
        var prefix = encodeURIComponent(parameter) + '=';
        var pars = urlparts[1].split(/[&;]/g);
        for (var i = pars.length; i-- > 0;) {
            if (pars[i].lastIndexOf(prefix, 0) !== -1) {
                pars.splice(i, 1);
            }
        }
        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
    return url;
}



function select_sort() {
    var select_sort_value = $("#select_sort").val();
    var url = removeURLParameter(window.location.href, "sort_type");
    window.location = url + "?sort_type=" + select_sort_value;
}



$(document).ready(
    function() {
        var urlParams = new URLSearchParams(window.location.search);
        if (urlParams == "") {
            localStorage.clear();
            $("#filter_delete").css("display", "none");
        }
        else {
            $("#filter_delete").css("display", "inline-block"); 
        }
        $('input:checkbox').on('click', function() {
            var fav, favs = [];
            $('input:checkbox').each(function() {
                fav = { id: $(this).attr('id'), value: $(this).prop('checked') };
                favs.push(fav);
            })
            localStorage.setItem("favorites", JSON.stringify(favs));
        })
        var favorites = JSON.parse(localStorage.getItem('favorites'));
        for (var i = 0; i < favorites.length; i++) {
            $('#' + favorites[i].id).prop('checked', favorites[i].value);
        }
    }
);

