function Nav({ currentPage, setPage, theme, toggleTheme }) {
    return (
        <nav className="fixed top-0 left-0 w-[150px] h-screen flex flex-col p-[20px_25px] bg-[#fff8eb] dark:bg-gradient-to-b dark:from-[#1a1a1a] dark:to-[#121212] box-border shadow-[2px_0_15px_rgba(242,142,43,0.08)] dark:shadow-[2px_0_15px_rgba(242,142,43,0.15)] z-[100] overflow-y-auto transition-colors duration-300">
            <div className="font-[Segoe_UI,Tahoma,Geneva,Verdana,sans-serif] text-[22px] font-bold text-[#e15759] text-center mb-[30px] mt-[10px] tracking-[1px]">
                Menu
            </div>
            {["cv", "projects", "certs"].map((page) => (
                <a
                    key={page}
                    href="#"
                    onClick={(e) => {
                        e.preventDefault();
                        setPage(page);
                    }}
                    className={`my-[8px] p-[12px_20px] rounded-[12px] font-[Segoe_UI,Tahoma,Geneva,Verdana,sans-serif] font-semibold text-[16px] tracking-[0.5px] text-center bg-transparent border-none transition-all duration-300 ease-[cubic-bezier(0.25,0.8,0.25,1)] cursor-pointer block hover:bg-[rgba(225,87,89,0.1)] hover:text-[#f28e2b] hover:shadow-[inset_2px_0_0_#f28e2b] hover:scale-105 ${currentPage === page
                            ? "text-[#f28e2b] bg-[rgba(225,87,89,0.1)] dark:text-[#f28e2b]"
                            : "text-[#e15759] dark:text-[#e0e0e0]"
                        }`}
                >
                    {page === "certs" ? "Cert" : page.charAt(0).toUpperCase() + page.slice(1)}
                </a>
            ))}
            <div className="flex-grow"></div>
            <button
                onClick={toggleTheme}
                className="w-full mt-auto mb-[20px] p-[10px] bg-transparent border-2 border-[#e15759] text-[#e15759] dark:border-[#f28e2b] dark:text-[#f28e2b] rounded-[8px] cursor-pointer font-bold transition-all duration-300 text-center hover:bg-[#e15759] hover:text-white dark:hover:bg-[#f28e2b] dark:hover:text-[#121212] hover:-translate-y-[2px] hover:shadow-[0_4px_10px_rgba(225,87,89,0.3)] dark:hover:shadow-[0_4px_10px_rgba(242,142,43,0.3)]"
            >
                {theme === "light" ? "Dark Mode" : "Light Mode"}
            </button>
        </nav>
    );
}

export default Nav;
