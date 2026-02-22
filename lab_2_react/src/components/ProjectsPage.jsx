import Footer from "./Footer";

function ProjectsPage() {
    return (
        <div className="ml-[150px] w-[calc(100%-150px)] box-border">
            <header className="flex justify-center items-center bg-[#fffbf4] text-[#333] drop-shadow-[1px_1px_2px_rgba(255,255,255,0.8)]" style={{ background: "#fffbf4 url('/firework_blue.svg') repeat", backgroundSize: "300px 300px" }}>
                <h1 className="m-0 py-[20px] font-sans font-bold text-3xl">My Projects</h1>
            </header>
            <main className="block">
                <div
                    className="flex flex-col justify-center items-center min-h-[calc(100vh-60px)] p-[40px] max-[768px]:p-[20px] w-full box-border"
                    style={{ background: "#fffbf4 url('/firework_blue.svg') repeat", backgroundSize: "300px 300px" }}
                >
                    <div className="grid grid-cols-3 max-[1200px]:grid-cols-2 max-[768px]:grid-cols-1 gap-[30px] w-full max-w-[1100px]">
                        <a href="#" className="group relative flex flex-col items-center text-center p-[30px_25px] rounded-[20px] bg-[rgba(255,255,255,0.6)] backdrop-blur-[12px] border border-solid border-[rgba(255,255,255,0.8)] no-underline text-[#2c3e50] shadow-[0_8px_32px_rgba(9,132,227,0.08)] overflow-hidden transition-all duration-400 ease-[cubic-bezier(0.25,0.8,0.25,1)] hover:-translate-y-[10px] hover:shadow-[0_15px_40px_rgba(9,132,227,0.15)] hover:bg-[rgba(255,255,255,0.85)] hover:border-[#0984e3]">
                            <div className="absolute inset-0 bg-gradient-to-br from-[rgba(255,255,255,0.4)] to-[rgba(255,255,255,0)] z-[1] pointer-events-none"></div>

                            <div className="text-[40px] mb-[20px] z-[2] transition-transform duration-300 ease-in-out group-hover:scale-[1.15]">🛡️</div>
                            <h3 className="m-[0_0_15px_0] text-[20px] text-[#0984e3] z-[2]">Enterprise Zero Trust</h3>
                            <p className="m-0 text-[14px] leading-[1.6] text-[#555] z-[2]">
                                Designed and documented a high-availability infrastructure using
                                HashiCorp Boundary.
                            </p>
                        </a>
                        <a href="#" className="group relative flex flex-col items-center text-center p-[30px_25px] rounded-[20px] bg-[rgba(255,255,255,0.6)] backdrop-blur-[12px] border border-solid border-[rgba(255,255,255,0.8)] no-underline text-[#2c3e50] shadow-[0_8px_32px_rgba(9,132,227,0.08)] overflow-hidden transition-all duration-400 ease-[cubic-bezier(0.25,0.8,0.25,1)] hover:-translate-y-[10px] hover:shadow-[0_15px_40px_rgba(9,132,227,0.15)] hover:bg-[rgba(255,255,255,0.85)] hover:border-[#0984e3]">
                            <div className="absolute inset-0 bg-gradient-to-br from-[rgba(255,255,255,0.4)] to-[rgba(255,255,255,0)] z-[1] pointer-events-none"></div>
                            <div className="text-[40px] mb-[20px] z-[2] transition-transform duration-300 ease-in-out group-hover:scale-[1.15]">☁️</div>
                            <h3 className="m-[0_0_15px_0] text-[20px] text-[#0984e3] z-[2]">Infrastructure as Code</h3>
                            <p className="m-0 text-[14px] leading-[1.6] text-[#555] z-[2]">
                                Managed end-to-end deployment via GitLab CI/CD, Terraform, and
                                Helm.
                            </p>
                        </a>
                        <a href="#" className="group relative flex flex-col items-center text-center p-[30px_25px] rounded-[20px] bg-[rgba(255,255,255,0.6)] backdrop-blur-[12px] border border-solid border-[rgba(255,255,255,0.8)] no-underline text-[#2c3e50] shadow-[0_8px_32px_rgba(9,132,227,0.08)] overflow-hidden transition-all duration-400 ease-[cubic-bezier(0.25,0.8,0.25,1)] hover:-translate-y-[10px] hover:shadow-[0_15px_40px_rgba(9,132,227,0.15)] hover:bg-[rgba(255,255,255,0.85)] hover:border-[#0984e3]">
                            <div className="absolute inset-0 bg-gradient-to-br from-[rgba(255,255,255,0.4)] to-[rgba(255,255,255,0)] z-[1] pointer-events-none"></div>
                            <div className="text-[40px] mb-[20px] z-[2] transition-transform duration-300 ease-in-out group-hover:scale-[1.15]">👁️</div>
                            <h3 className="m-[0_0_15px_0] text-[20px] text-[#0984e3] z-[2]">Observability & Audit</h3>
                            <p className="m-0 text-[14px] leading-[1.6] text-[#555] z-[2]">
                                Built a centralized logging pipeline using Splunk, Prometheus,
                                and Grafana.
                            </p>
                        </a>
                        <a href="#" className="group relative flex flex-col items-center text-center p-[30px_25px] rounded-[20px] bg-[rgba(255,255,255,0.6)] backdrop-blur-[12px] border border-solid border-[rgba(255,255,255,0.8)] no-underline text-[#2c3e50] shadow-[0_8px_32px_rgba(9,132,227,0.08)] overflow-hidden transition-all duration-400 ease-[cubic-bezier(0.25,0.8,0.25,1)] hover:-translate-y-[10px] hover:shadow-[0_15px_40px_rgba(9,132,227,0.15)] hover:bg-[rgba(255,255,255,0.85)] hover:border-[#0984e3]">
                            <div className="absolute inset-0 bg-gradient-to-br from-[rgba(255,255,255,0.4)] to-[rgba(255,255,255,0)] z-[1] pointer-events-none"></div>
                            <div className="text-[40px] mb-[20px] z-[2] transition-transform duration-300 ease-in-out group-hover:scale-[1.15]">🎁</div>
                            <h3 className="m-[0_0_15px_0] text-[20px] text-[#0984e3] z-[2]">Wishlist SaaS</h3>
                            <p className="m-0 text-[14px] leading-[1.6] text-[#555] z-[2]">
                                Scalable gift-tracking platform with resilient scraping engine
                                and containerized backend.
                            </p>
                        </a>
                        <a href="#" className="group relative flex flex-col items-center text-center p-[30px_25px] rounded-[20px] bg-[rgba(255,255,255,0.6)] backdrop-blur-[12px] border border-solid border-[rgba(255,255,255,0.8)] no-underline text-[#2c3e50] shadow-[0_8px_32px_rgba(9,132,227,0.08)] overflow-hidden transition-all duration-400 ease-[cubic-bezier(0.25,0.8,0.25,1)] hover:-translate-y-[10px] hover:shadow-[0_15px_40px_rgba(9,132,227,0.15)] hover:bg-[rgba(255,255,255,0.85)] hover:border-[#0984e3]">
                            <div className="absolute inset-0 bg-gradient-to-br from-[rgba(255,255,255,0.4)] to-[rgba(255,255,255,0)] z-[1] pointer-events-none"></div>
                            <div className="text-[40px] mb-[20px] z-[2] transition-transform duration-300 ease-in-out group-hover:scale-[1.15]">🤖</div>
                            <h3 className="m-[0_0_15px_0] text-[20px] text-[#0984e3] z-[2]">Multi-Agent System</h3>
                            <p className="m-0 text-[14px] leading-[1.6] text-[#555] z-[2]">
                                Orchestrating specialized LLM agents for automated infrastructure
                                remediation.
                            </p>
                        </a>
                        <a href="#" className="group relative flex flex-col items-center text-center p-[30px_25px] rounded-[20px] bg-[rgba(255,255,255,0.6)] backdrop-blur-[12px] border border-solid border-[rgba(255,255,255,0.8)] no-underline text-[#2c3e50] shadow-[0_8px_32px_rgba(9,132,227,0.08)] overflow-hidden transition-all duration-400 ease-[cubic-bezier(0.25,0.8,0.25,1)] hover:-translate-y-[10px] hover:shadow-[0_15px_40px_rgba(9,132,227,0.15)] hover:bg-[rgba(255,255,255,0.85)] hover:border-[#0984e3]">
                            <div className="absolute inset-0 bg-gradient-to-br from-[rgba(255,255,255,0.4)] to-[rgba(255,255,255,0)] z-[1] pointer-events-none"></div>
                            <div className="text-[40px] mb-[20px] z-[2] transition-transform duration-300 ease-in-out group-hover:scale-[1.15]">🔒</div>
                            <h3 className="m-[0_0_15px_0] text-[20px] text-[#0984e3] z-[2]">DevSecOps Pipeline</h3>
                            <p className="m-0 text-[14px] leading-[1.6] text-[#555] z-[2]">
                                Automated security gates including SAST, SCA, and DAST in CI/CD.
                            </p>
                        </a>
                    </div>
                </div>
            </main>
            <Footer bgClass="bg-[#f0f7f4]" textClass="text-[#0984e3]" />
        </div>
    );
}

export default ProjectsPage;
