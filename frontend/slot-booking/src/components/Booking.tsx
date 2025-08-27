import { useState } from "react";

function Booking() {
  const [canceled, setCanceled] = useState(false);

  const cancel_booking = () => {
    setCanceled(true);
  };

  return (
    <div className="h-32 w-[75rem] flex justify-center items-center overflow-visible">
      <div
        className={`
          relative h-30 w-6xl bg-gradient-to-r from-black to-gray-700
          flex justify-between items-center rounded-2xl
          transition-all duration-700 ease-in-out
          ${canceled ? "scale-105 rotate-x-360 duration-[2000ms]" : "hover:scale-105"}
        `}
        style={{
          transformStyle: "preserve-3d", // required for 3D flip
        }}
      >
        {/* Image */}
        <div className="h-20 w-20 ml-3 rounded-full overflow-hidden flex justify-center items-center">
          <img
            src="data:image/jpeg;base64,...yourBase64..."
            alt=""
          />
        </div>

        {/* Title */}
        <div className="text-yellow-500 font-black text-3xl">Tekken 8</div>

        {/* Time */}
        <div className="text-white text-2xl">07:00PM - 08:30PM</div>

        {/* Cancel Button */}
        <div>
          <button
            onClick={cancel_booking}
            className={`
              text-white text-2xl font-bold h-15 w-50 mr-5 rounded-full transition-colors duration-300
              ${canceled ? "bg-green-500" : "bg-red-500 hover:bg-red-600 cursor-pointer"}
            `}
          >
            {canceled ? "Canceled" : "Cancel Booking"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Booking;
