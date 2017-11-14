function toggleDetailsView(note_id, link_id) {
        var item = document.getElementById(note_id);
        var link = document.getElementById(link_id);

        console.log(note_id);
        console.log(item);

        if (item.style.display == "block") {
            item.style.display = "none";
            link.innerHTML = "+Details";
            link.style.color = "#304c89";

        } else {
            item.style.display = "block";
            link.innerHTML = "-Details";
            link.style.color = "#F90707";
        }
    }
