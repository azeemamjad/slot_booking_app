import React, { useState } from 'react';

// --- ICONS (Self-contained SVGs) ---
const ClockIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4 mr-2 text-yellow-400">
        <circle cx="12" cy="12" r="10"></circle>
        <polyline points="12 6 12 12 16 14"></polyline>
    </svg>
);

const UsersIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4 mr-2 text-yellow-400">
        <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
        <circle cx="9" cy="7" r="4"></circle>
        <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
    </svg>
);


// --- REUSABLE SLOT CARD COMPONENT ---
function SlotCard() {
    // --- STATE MANAGEMENT ---
    // Total capacity for the gaming slot
    const capacity = 4;
    // State to track the number of currently booked slots
    const [bookedCount, setBookedCount] = useState(2);
    // State to track if the current user has made a booking
    const [isBookedByUser, setIsBookedByUser] = useState(false);
    // State for displaying a confirmation or error message
    const [statusMessage, setStatusMessage] = useState('');

    // --- DERIVED STATE ---
    // Calculate if the slot is full
    const isFull = bookedCount >= capacity;
    // Calculate remaining spots
    const spotsLeft = capacity - bookedCount;

    // --- EVENT HANDLER ---
    const handleBooking = () => {
        // Prevent booking if the slot is full or the user has already booked
        if (isFull || isBookedByUser) {
            return;
        }

        // Update state to reflect the new booking
        setBookedCount(prevCount => prevCount + 1);
        setIsBookedByUser(true);
        setStatusMessage('BOOKING CONFIRMED! GET READY FOR THE NEXT BATTLE.');

        // Clear the message after 4 seconds
        setTimeout(() => {
            setStatusMessage('');
        }, 4000);
    };
    
    // --- DYNAMIC STYLING & CONTENT ---
    const buttonText = isBookedByUser ? 'YOUR SPOT IS SECURED' : isFull ? 'SLOT FULL' : 'BOOK YOUR SPOT';
    const buttonClasses = `
        w-full text-center font-bold text-lg py-4 px-6 rounded-lg transition-all duration-300 ease-in-out
        focus:outline-none focus:ring-4 focus:ring-yellow-500/50
        ${isBookedByUser 
            ? 'bg-green-500 text-white cursor-default' 
            : isFull 
            ? 'bg-gray-700 text-gray-400 cursor-not-allowed' 
            : 'bg-gradient-to-r from-red-600 to-red-800 text-white hover:from-red-700 hover:to-red-800 transform hover:scale-105'
        }
    `;

    return (
        <div className="w-full max-w-sm bg-gray-800 border-2 border-yellow-400 rounded-xl shadow-2xl shadow-yellow-500/10 overflow-hidden font-sans">
            {/* Card Header with Game Title */}
            <div className="p-5 bg-gradient-to-r from-black via-gray-900 to-black">
                <h1 className="text-3xl font-extrabold text-center text-white tracking-wider uppercase" style={{ fontFamily: '"Tekken", sans-serif' }}>
                    TEKKEN 8
                </h1>
                <p className="text-center text-yellow-400 font-semibold">BATTLE HUB</p>
            </div>

            {/* Main Content Area */}
            <div className="p-6">
                {/* Slot Details */}
                <div className="mb-6 text-white">
                    <h2 className="text-xl font-bold mb-4 border-b-2 border-yellow-400/30 pb-2">King of the Iron Fist Tournament</h2>
                    <div className="flex items-center mb-3">
                        <ClockIcon />
                        <span>Today, 8:30 PM - 9:30 PM</span>
                    </div>
                    <div className="flex items-center">
                        <UsersIcon />
                        <span>Nexus Gaming Arena, Lahore</span>
                    </div>
                </div>

                {/* Capacity Indicator */}
                <div className="mb-6">
                    <div className="flex justify-between items-center mb-2 text-sm font-semibold">
                        <span className="text-yellow-400">Capacity</span>
                        <span className="text-white">{bookedCount} / {capacity}</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-3">
                        <div 
                            className="bg-yellow-400 h-3 rounded-full transition-all duration-500" 
                            style={{ width: `${(bookedCount / capacity) * 100}%` }}
                        ></div>
                    </div>
                     <p className="text-right text-white mt-1 text-sm">{spotsLeft > 0 ? `${spotsLeft} spot${spotsLeft > 1 ? 's' : ''} left` : "No spots available"}</p>
                </div>

                {/* Action Button */}
                <button 
                    onClick={handleBooking}
                    disabled={isFull || isBookedByUser}
                    className={buttonClasses}
                >
                    {buttonText}
                </button>

                {/* Status Message */}
                {statusMessage && (
                    <p className="mt-4 text-center text-green-400 font-semibold text-sm animate-pulse">
                        {statusMessage}
                    </p>
                )}
            </div>
        </div>
    );
}

export default SlotCard;
