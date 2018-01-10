function profitBGcolor(pclass, profit) {

    var x = document.getElementsByClassName(pclass);
    var pn = Number(profit);
    var i;

    if (pn > 0.00) {

        for (i = 0; i < x.length; i++) {
            x[i].style.backgroundColor = "#00A300";
        }

    } else {
         for (i = 0; i < x.length; i++) {
            x[i].style.backgroundColor = "#F73A45";
        }
    }
}