function Footer({ bgClass = "bg-[#fff8eb]", textClass = "text-[#e15759]" }) {
    return (
        <footer className={`flex justify-center items-center h-[60px] ${bgClass} ${textClass} font-[Segoe_UI,Tahoma,Geneva,Verdana,sans-serif] text-[14px] tracking-[1px] shadow-[0_-2px_10px_rgba(242,142,43,0.1)]`}>
            Andrew Kizim 2026
        </footer>
    );
}

export default Footer;
