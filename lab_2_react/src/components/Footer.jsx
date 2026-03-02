import { useState, useEffect } from "react";

function Footer({ bgClass = "bg-[#fff8eb]", textClass = "text-[#e15759]" }) {
    const [systemInfo, setSystemInfo] = useState("");

    useEffect(() => {
        const info = navigator.userAgent;
        localStorage.setItem("system_info", info);

        const savedInfo = localStorage.getItem("system_info");
        setSystemInfo(savedInfo);
    }, []);

    return (
        <footer className={`flex flex-col justify-center items-center py-[20px] px-[15px] min-h-[80px] text-center ${bgClass} ${textClass} font-[Segoe_UI,Tahoma,Geneva,Verdana,sans-serif] text-[14px] tracking-[1px] shadow-[0_-2px_10px_rgba(242,142,43,0.1)] transition-colors duration-300`}>
            <div className="font-semibold mb-[8px]">Andrew Kizim 2026</div>
            {systemInfo && (
                <div className="text-[11px] opacity-75 max-w-[800px] leading-relaxed break-words">
                    <span className="font-bold mr-[4px]">System:</span>{systemInfo}
                </div>
            )}
        </footer>
    );
}

export default Footer;
