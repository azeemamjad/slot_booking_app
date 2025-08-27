import { useMemo } from "react";

function Loading() {
  const text = "Loading";

  // Split text into characters once
  const chars = useMemo(() => text.split(""), [text]);
  const styles = `@keyframes bounce-seq {
                0%, 80%, 100% {
                    transform: translateY(0);
                }
                40% {
                    transform: translateY(-12px); /* lift up */
                }
                }

                .animate-bounce-seq {
                animation: bounce-seq 1s infinite;
            }`

  return (
    <div className="absolute top-0 left-0 w-screen h-screen bg-white/30 backdrop-blur-sm z-50 flex justify-center items-center">
        <style>
            {styles}
        </style>
      <h1 className="flex gap-1 text-sm font-bold text-black">
        {chars.map((char, i) => (
          <span
            key={i}
            className="inline-block animate-bounce-seq"
            style={{ animationDelay: `${i * 0.15}s` }}
          >
            {char}
          </span>
        ))}
      </h1>
    </div>
  );
}

export default Loading;
