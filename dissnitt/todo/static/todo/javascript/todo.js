

function toggleItemView(list_id, link_id, dstyle) {

        var items = document.getElementById(list_id);
        var link = document.getElementById(link_id);

        if (items.style.display == dstyle) {
            items.style.display = "none";
            link.innerHTML = "+";
            link.style.color = "#304c89";

        } else {
            items.style.display = dstyle;
            link.innerHTML = "-";
            link.style.color = "#5487AC";

        }
    }

function getCheckBox(item_id, comp){
    var item = document.getElementById(item_id);
    console.log(item_id)

    if (comp === "True") {
        item.innerHTML = "<img src='/static/todo/images/checked.png' class='cbox' alt='True'/>";

    } else {
        item.innerHTML = "<img src='/static/todo/images/unchecked.png' class='cbox' alt='False'/>";

    }

}
