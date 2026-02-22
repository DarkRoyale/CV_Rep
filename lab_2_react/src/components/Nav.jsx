function Nav({ currentPage, setPage }) {
    return (
        <nav className="fixed top-0 left-0 w-[150px] h-screen flex flex-col p-[20px_25px] bg-[#fff8eb] box-border shadow-[2px_0_15px_rgba(242,142,43,0.08)] z-[100] overflow-y-auto">
            <div className="font-[Segoe_UI,Tahoma,Geneva,Verdana,sans-serif] text-[22px] font-bold text-[#e15759] text-center mb-[30px] mt-[10px] tracking-[1px]">
                Menu
            </div>
            <a
                href="#"
                onClick={(e) => {
                    e.preventDefault();
                    setPage("cv");
                }}
                className={`my-[8px] p-[12px_20px] rounded-[12px] font-[Segoe_UI,Tahoma,Geneva,Verdana,sans-serif] font-semibold text-[16px] tracking-[0.5px] text-center bg-transparent border-none transition-all duration-300 ease-[cubic-bezier(0.25,0.8,0.25,1)] cursor-pointer block hover:bg-[rgba(225,87,89,0.1)] hover:text-[#f28e2b] hover:scale-105 ${currentPage === "cv"
                        ? "text-[#f28e2b] bg-[rgba(225,87,89,0.1)]"
                        : "text-[#e15759]"
                    }`}
            >
                CV
            </a>
            <a
                href="#"
                onClick={(e) => {
                    e.preventDefault();
                    setPage("projects");
                }}
                className={`my-[8px] p-[12px_20px] rounded-[12px] font-[Segoe_UI,Tahoma,Geneva,Verdana,sans-serif] font-semibold text-[16px] tracking-[0.5px] text-center bg-transparent border-none transition-all duration-300 ease-[cubic-bezier(0.25,0.8,0.25,1)] cursor-pointer block hover:bg-[rgba(225,87,89,0.1)] hover:text-[#f28e2b] hover:scale-105 ${currentPage === "projects"
                        ? "text-[#f28e2b] bg-[rgba(225,87,89,0.1)]"
                        : "text-[#e15759]"
                    }`}
            >
                Projects
            </a>
            <a
                href="#"
                onClick={(e) => {
                    e.preventDefault();
                    setPage("certs");
                }}
                className={`my-[8px] p-[12px_20px] rounded-[12px] font-[Segoe_UI,Tahoma,Geneva,Verdana,sans-serif] font-semibold text-[16px] tracking-[0.5px] text-center bg-transparent border-none transition-all duration-300 ease-[cubic-bezier(0.25,0.8,0.25,1)] cursor-pointer block hover:bg-[rgba(225,87,89,0.1)] hover:text-[#f28e2b] hover:scale-105 ${currentPage === "certs"
                        ? "text-[#f28e2b] bg-[rgba(225,87,89,0.1)]"
                        : "text-[#e15759]"
                    }`}
            >
                Cert
            </a>
        </nav>
    );
}

export default Nav;
