function Header() {
  return (
    <header
      className={`flex justify-center items-center text-[#333] drop-shadow-[1px_1px_2px_rgba(255,255,255,0.8)] bg-[#fffbf4] bg-[url('/firework.svg')] dark:bg-[#121212] dark:bg-[url('/firework-dark.svg')] bg-[length:300px_300px] dark:text-white dark:drop-shadow-[2px_2px_4px_rgba(0,0,0,0.8)] dark:border-b dark:border-b-[rgba(242,142,43,0.2)] transition-colors duration-300`}
    >
      <h1 className="m-[20px_0] text-[2em] font-bold">Andrii Kizim. CV</h1>
    </header>
  );
}
export default Header;
