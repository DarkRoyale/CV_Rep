function PersonalInfo() {
  return (
    <>
      <section className="block mb-[22px] last-of-type:mb-0">
        <h1 className="m-[0_0_8px] pb-[4px] border-b border-solid border-[#2f2f2f] text-[14px] tracking-[0.07em] uppercase font-bold">Andrii Kizim</h1>
        <div className="m-[6px_0_8px] leading-[1.6]">
          <div><strong>Location:</strong> Lviv, Ukraine (Open to remote and hybrid roles)</div>
          <div><strong>Email:</strong> email@gmail.com </div>
          <div><strong>LinkedIn:</strong> https://www.linkedin.com/in/andrew-kizim-502793292/</div>
          <div><strong>GitHub:</strong> https://github.com/DarkRoyale</div>
        </div>
      </section>

      <section className="block mb-[22px] last-of-type:mb-0">
        <h1 className="m-[0_0_8px] pb-[4px] border-b border-solid border-[#2f2f2f] text-[14px] tracking-[0.07em] uppercase font-bold">Professional Summary</h1>
        <p className="m-[6px_0_8px]">
          Cybersecurity and security engineering specialist focused on secure architecture, resilient infrastructure, and automation-driven delivery.
        </p>
        <ul className="m-[4px_0_0_18px] p-0 list-disc">
          <li className="mb-[4px]">
            <strong>Role focus:</strong> Cybersecurity, Security Engineering, DevSecOps, Security Architect
          </li>
        </ul>
      </section>
    </>
  );
}
export default PersonalInfo;
