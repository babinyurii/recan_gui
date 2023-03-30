function validateWindow() {
   let x = Number(document.forms["dist_plot_form"]["window_size"].value);
   if (x < 100) {
       alert ("window must be > 100");
       return false;
  }
}
