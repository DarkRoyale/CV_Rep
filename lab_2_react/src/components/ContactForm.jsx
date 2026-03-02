import { useState, useEffect } from "react";

function ContactForm() {
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => {
            setIsOpen(true);
        }, 60000);

        return () => clearTimeout(timer);
    }, []);

    if (!isOpen) return null;

    return (
        <div
            className="fixed inset-0 z-[1000] flex items-center justify-center bg-black/50 backdrop-blur-sm"
            onClick={(e) => {
                if (e.target.dataset.overlay) setIsOpen(false);
            }}
            data-overlay="true"
        >
            <div className="relative bg-white w-[80%] max-w-[500px] p-[30px] rounded-[12px] shadow-[0_5px_15px_rgba(0,0,0,0.3)] font-[Segoe_UI,Tahoma,Geneva,Verdana,sans-serif]">
                <button
                    onClick={() => setIsOpen(false)}
                    className="absolute top-[10px] right-[20px] text-[#aaa] text-[28px] font-bold cursor-pointer hover:text-[#e15759] transition-colors"
                >
                    &times;
                </button>

                <h2 className="text-[#333] text-[24px] font-bold mt-0 mb-[20px] pb-[10px] border-b-2 border-[#f28e2b]">
                    Feedback
                </h2>

                <form action="https://formspree.io/f/xvzbnyka" method="POST">
                    <div className="mb-[15px]">
                        <label className="block mb-[5px] font-bold text-[#333]" htmlFor="name">Name:</label>
                        <input className="w-full p-[10px] border border-[#ccc] rounded-[6px] box-border font-inherit focus:outline-none focus:border-[#f28e2b] focus:ring-1 focus:ring-[#f28e2b]" type="text" id="name" name="name" required />
                    </div>

                    <div className="mb-[15px]">
                        <label className="block mb-[5px] font-bold text-[#333]" htmlFor="email">Email:</label>
                        <input className="w-full p-[10px] border border-[#ccc] rounded-[6px] box-border font-inherit focus:outline-none focus:border-[#f28e2b] focus:ring-1 focus:ring-[#f28e2b]" type="email" id="email" name="email" required />
                    </div>

                    <div className="mb-[15px]">
                        <label className="block mb-[5px] font-bold text-[#333]" htmlFor="phone">Phone:</label>
                        <input className="w-full p-[10px] border border-[#ccc] rounded-[6px] box-border font-inherit focus:outline-none focus:border-[#f28e2b] focus:ring-1 focus:ring-[#f28e2b]" type="tel" id="phone" name="phone" />
                    </div>

                    <div className="mb-[15px]">
                        <label className="block mb-[5px] font-bold text-[#333]" htmlFor="message">Message:</label>
                        <textarea className="w-full p-[10px] border border-[#ccc] rounded-[6px] box-border font-inherit min-h-[100px] focus:outline-none focus:border-[#f28e2b] focus:ring-1 focus:ring-[#f28e2b]" id="message" name="message" rows="4" required></textarea>
                    </div>

                    <button type="submit" className="w-full bg-[#e15759] text-white p-[12px_20px] border-none rounded-[6px] cursor-pointer text-[16px] font-bold transition-colors hover:bg-[#c0392b]">
                        Submit
                    </button>
                </form>
            </div>
        </div>
    );
}

export default ContactForm;
