

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

