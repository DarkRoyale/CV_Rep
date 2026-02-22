import Footer from "./Footer";

function CertPage() {
    return (
        <div className="ml-[150px] w-[calc(100%-150px)] box-border">
            <header className="flex justify-center items-center bg-[#fffbf4] text-[#333] drop-shadow-[1px_1px_2px_rgba(255,255,255,0.8)]" style={{ background: "#fffbf4 url('/firework_gold.svg') repeat", backgroundSize: "300px 300px" }}>
                <h1 className="m-0 py-[20px] font-sans font-bold text-3xl">My Certifications</h1>
            </header>
            <main className="block">
                <div
                    className="flex flex-col justify-center items-center min-h-[calc(100vh-60px)] p-[40px] w-full box-border"
                    style={{ background: "#fffbf4 url('/firework_gold.svg') repeat", backgroundSize: "300px 300px" }}
                >
                    <div className="grid grid-cols-2 max-[900px]:grid-cols-1 gap-[30px] w-full max-w-[900px]">
                        <a href="#" className="group relative flex flex-row max-[900px]:flex-col max-[900px]:text-center items-center p-[30px] rounded-[16px] bg-[rgba(255,255,255,0.7)] backdrop-blur-[15px] border border-solid border-[rgba(255,215,0,0.5)] no-underline text-[#2c3e50] shadow-[0_8px_32px_rgba(243,156,18,0.1)] overflow-hidden transition-all duration-400 ease-[cubic-bezier(0.25,0.8,0.25,1)] hover:-translate-y-[8px] hover:shadow-[0_15px_40px_rgba(243,156,18,0.2)] hover:bg-[rgba(255,255,255,0.9)] hover:border-[#f39c12]">
                            <div className="absolute inset-0 bg-gradient-to-br from-[rgba(255,255,255,0.5)] to-[rgba(255,255,255,0)] z-[1] pointer-events-none"></div>

                            <div className="text-[50px] mr-[25px] max-[900px]:mr-0 max-[900px]:mb-[20px] z-[2] transition-transform duration-300 ease-in-out drop-shadow-[0_2px_4px_rgba(243,156,18,0.3)] group-hover:scale-[1.1] group-hover:rotate-[5deg]">🥇</div>
                            <div className="flex flex-col z-[2]">
                                <h3 className="m-[0_0_10px_0] text-[22px] text-[#d35400]">Block</h3>
                                <p className="m-0 text-[15px] leading-[1.5] text-[#555] italic">Block</p>
                                <div className="mt-[10px] text-[13px] text-[#7f8c8d] font-semibold">Block</div>
                            </div>
                        </a>

                        <a href="#" className="group relative flex flex-row max-[900px]:flex-col max-[900px]:text-center items-center p-[30px] rounded-[16px] bg-[rgba(255,255,255,0.7)] backdrop-blur-[15px] border border-solid border-[rgba(255,215,0,0.5)] no-underline text-[#2c3e50] shadow-[0_8px_32px_rgba(243,156,18,0.1)] overflow-hidden transition-all duration-400 ease-[cubic-bezier(0.25,0.8,0.25,1)] hover:-translate-y-[8px] hover:shadow-[0_15px_40px_rgba(243,156,18,0.2)] hover:bg-[rgba(255,255,255,0.9)] hover:border-[#f39c12]">
                            <div className="absolute inset-0 bg-gradient-to-br from-[rgba(255,255,255,0.5)] to-[rgba(255,255,255,0)] z-[1] pointer-events-none"></div>
                            <div className="text-[50px] mr-[25px] max-[900px]:mr-0 max-[900px]:mb-[20px] z-[2] transition-transform duration-300 ease-in-out drop-shadow-[0_2px_4px_rgba(243,156,18,0.3)] group-hover:scale-[1.1] group-hover:rotate-[5deg]">🏆</div>
                            <div className="flex flex-col z-[2]">
                                <h3 className="m-[0_0_10px_0] text-[22px] text-[#d35400]">Block</h3>
                                <p className="m-0 text-[15px] leading-[1.5] text-[#555] italic">Block</p>
                                <div className="mt-[10px] text-[13px] text-[#7f8c8d] font-semibold">Block</div>
                            </div>
                        </a>

                        <a href="#" className="group relative flex flex-row max-[900px]:flex-col max-[900px]:text-center items-center p-[30px] rounded-[16px] bg-[rgba(255,255,255,0.7)] backdrop-blur-[15px] border border-solid border-[rgba(255,215,0,0.5)] no-underline text-[#2c3e50] shadow-[0_8px_32px_rgba(243,156,18,0.1)] overflow-hidden transition-all duration-400 ease-[cubic-bezier(0.25,0.8,0.25,1)] hover:-translate-y-[8px] hover:shadow-[0_15px_40px_rgba(243,156,18,0.2)] hover:bg-[rgba(255,255,255,0.9)] hover:border-[#f39c12]">
                            <div className="absolute inset-0 bg-gradient-to-br from-[rgba(255,255,255,0.5)] to-[rgba(255,255,255,0)] z-[1] pointer-events-none"></div>
                            <div className="text-[50px] mr-[25px] max-[900px]:mr-0 max-[900px]:mb-[20px] z-[2] transition-transform duration-300 ease-in-out drop-shadow-[0_2px_4px_rgba(243,156,18,0.3)] group-hover:scale-[1.1] group-hover:rotate-[5deg]">🏅</div>
                            <div className="flex flex-col z-[2]">
                                <h3 className="m-[0_0_10px_0] text-[22px] text-[#d35400]">Block</h3>
                                <p className="m-0 text-[15px] leading-[1.5] text-[#555] italic">Block</p>
                                <div className="mt-[10px] text-[13px] text-[#7f8c8d] font-semibold">Block</div>
                            </div>
                        </a>

                        <a href="#" className="group relative flex flex-row max-[900px]:flex-col max-[900px]:text-center items-center p-[30px] rounded-[16px] bg-[rgba(255,255,255,0.7)] backdrop-blur-[15px] border border-solid border-[rgba(255,215,0,0.5)] no-underline text-[#2c3e50] shadow-[0_8px_32px_rgba(243,156,18,0.1)] overflow-hidden transition-all duration-400 ease-[cubic-bezier(0.25,0.8,0.25,1)] hover:-translate-y-[8px] hover:shadow-[0_15px_40px_rgba(243,156,18,0.2)] hover:bg-[rgba(255,255,255,0.9)] hover:border-[#f39c12]">
                            <div className="absolute inset-0 bg-gradient-to-br from-[rgba(255,255,255,0.5)] to-[rgba(255,255,255,0)] z-[1] pointer-events-none"></div>
                            <div className="text-[50px] mr-[25px] max-[900px]:mr-0 max-[900px]:mb-[20px] z-[2] transition-transform duration-300 ease-in-out drop-shadow-[0_2px_4px_rgba(243,156,18,0.3)] group-hover:scale-[1.1] group-hover:rotate-[5deg]">🎖️</div>
                            <div className="flex flex-col z-[2]">
                                <h3 className="m-[0_0_10px_0] text-[22px] text-[#d35400]">Block</h3>
                                <p className="m-0 text-[15px] leading-[1.5] text-[#555] italic">Block</p>
                                <div className="mt-[10px] text-[13px] text-[#7f8c8d] font-semibold">Block</div>
                            </div>
                        </a>
                    </div>
                </div>
            </main>
            <Footer bgClass="bg-[#fff8eb]" textClass="text-[#e67e22]" />
        </div>
    );
}

export default CertPage;
