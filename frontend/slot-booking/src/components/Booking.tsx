import { useId } from "react";

function Booking(){

    const uuid = useId()
    
    const cancel_booking = () => {
        const btn = document.getElementById(`cancel-btn-${uuid}`);
        if (btn) {
            btn.innerHTML = "Canceled";
            btn.className = "text-white text-2xl font-bold h-15 w-50 mr-5 bg-green-500 rounded-full"
        }
    }
    return (
        <>
            <div className="h-32 w-[75rem] flex justify-center items-center">
                <div className="h-30 w-6xl bg-gradient-to-r from-0% to-30% hover:to-70% from-black to-gray-700 flex justify-between items-center rounded-2xl hover:h-32 hover:w-[75rem] transition-all duration-300">
                        <div className="h-20 w-20 ml-3 rounded-full overflow-hidden flex justify-center items-center">
                            <img src="data:image/jpeg;base64,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" alt="" />
                        </div>
                        <div className="text-yellow-500 font-black text-3xl">
                            Tekken 8
                        </div>
                        <div className="text-white text-2xl">
                            07:00PM - 08:30PM
                        </div>
                        <div>
                            <button onClick={() => { cancel_booking() }} id={`cancel-btn-${uuid}`} className="text-white text-2xl font-bold h-15 cursor-pointer w-50 mr-5 bg-red-500 hover:bg-red-600 rounded-full">Cancel Booking</button>
                        </div>
                </div>
            </div>
        </>
    )
}


export default Booking;