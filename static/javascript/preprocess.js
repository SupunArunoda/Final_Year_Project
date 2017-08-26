/**
 * Created by Buddhi on 8/20/2017.
 */

function runPreprocessScript(file) {
    $.ajax({
        type: "POST",
        url: "../../../model/cluster/Hierarchical.py",
        data: {param: 'buddhi'}
    }).done(function (response) {
        console.log(response);
    });
}

