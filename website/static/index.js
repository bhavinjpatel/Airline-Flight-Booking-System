function deleteBooking(bookingId) {
  fetch("/delete-booking", {
    method: "POST",
    body: JSON.stringify({ bookingId: bookingId }),
  }).then((_res) => {
    window.location.href = "/customer/my_bookings";
  });
}
