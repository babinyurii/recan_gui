function validateWindow() {
    let window_size = Number(document.forms["dist_plot_form"]["window_size"].value);
    let window_shift = Number(document.forms["dist_plot_form"]["window_shift"].value);

    let region_start = Number(document.forms["dist_plot_form"]["region_start"].value);
    let region_end = Number(document.forms["dist_plot_form"]["region_end"].value);
   
    if (window_size < window_shift) {
        alert ("window size should be greater than window shift");
        return false;
    }

    if (region_start >= region_end) {
        alert ("selected region start should be less than the region end");
        return false;
    }

    else {
        return true;
    }
}



