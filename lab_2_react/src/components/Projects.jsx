function Projects() {
  return (
    <section className="block mb-[22px] last-of-type:mb-0">
      <h1 className="m-[0_0_8px] pb-[4px] border-b border-solid border-[#2f2f2f] text-[14px] tracking-[0.07em] uppercase font-bold">Projects</h1>
      <ul className="m-[4px_0_0_18px] p-0 list-disc">
        <li className="mb-[4px]">
          <strong>
            Kintsugi Protocol (KTN): Secure Satellite Data Transfer
          </strong>
          <p className="m-[6px_0_8px]">
            Developed during the <em>ActInSpace</em> hackathon. A
            secure-by-design protocol concept tailored for the unique
            constraints of satellite communications.
          </p>
          <ul className="m-[6px_0_0_18px] list-disc">
            <li className="mb-[4px]">
              Designed a resilient security architecture to ensure data
              confidentiality and integrity in high-latency environments.
            </li>
            <li className="mb-[4px]">
              Mitigated interception risks by implementing robust encryption and
              verification mechanisms.
            </li>
            <li className="mb-[4px]">
              Researched protocol adaptability for space-grade,
              radiation-hardened hardware.
            </li>
          </ul>
        </li>
        <li className="mb-[4px]">
          <strong>
            Enterprise Zero Trust Access Architecture (HashiCorp Boundary)
          </strong>
          <p className="m-[6px_0_8px]">
            Designed and documented a high-availability (HA) infrastructure for
            secure privileged access, integrating a complex ecosystem of
            security and monitoring tools.
          </p>
          <ul className="m-[6px_0_0_18px] list-disc">
            <li className="mb-[4px]">
              <strong>Identity & Access:</strong> Integrated
              <strong>Azure AD (OIDC/SCIM)</strong> for SSO and MFA,
              implementing
              <strong>Just-in-Time (JIT)</strong> credentials through
              <strong>HashiCorp Vault</strong> integration.
            </li>
            <li className="mb-[4px]">
              <strong>Infrastructure as Code:</strong> Managed end-to-end
              deployment via
              <strong>GitLab CI/CD</strong>, using
              <strong>Terraform</strong> and
              <strong>Helm</strong> for automated environment provisioning.
            </li>
            <li className="mb-[4px]">
              <strong>Security & Compliance:</strong> Designed a{" "}
              <strong>Defense-in-Depth</strong> network with
              <strong>DMZ, WAF</strong>, and micro-segmentation using
              <strong>Calico/Cilium</strong> Network Policies.
            </li>
            <li className="mb-[4px]">
              <strong>Observability & Audit:</strong> Built a centralized
              logging and monitoring pipeline using{" "}
              <strong>Splunk (SIEM)</strong>,<strong>Prometheus</strong>, and
              <strong>Grafana</strong> for real-time security auditing.
            </li>
            <li className="mb-[4px]">
              <strong>DevSecOps Pipeline:</strong> Automated security gates
              including
              <strong>SAST (tfsec)</strong>,<strong>SCA (Trivy)</strong>, and
              <strong>DAST (OWASP ZAP)</strong> to ensure supply chain security.
            </li>
          </ul>
        </li>
        <li className="mb-[4px]">
          <strong>
            Wishlist SaaS & Intelligent Data Extraction — In Progress
          </strong>
          <p className="m-[6px_0_8px]">
            Developing a scalable gift-tracking platform featuring a resilient
            scraping engine and containerized backend infrastructure.
          </p>
          <ul className="m-[6px_0_0_18px] list-disc">
            <li className="mb-[4px]">
              <strong>Containerized Environment:</strong>
              Orchestrated the entire application stack using
              <strong>Docker</strong>, ensuring seamless deployment and
              environment isolation for backend services.
            </li>
            <li className="mb-[4px]">
              <strong>Hybrid Parsing Engine:</strong>
              Engineered a two-tier data extraction system: a high-performance
              HTML parser for standard requests and an
              <strong>AI-driven fallback</strong> for complex, non-standard
              e-commerce structures.
            </li>
            <li className="mb-[4px]">
              <strong>Proxy & Traffic Management:</strong>
              Integrated <strong>Mobile Proxies</strong> to tunnel full HTML
              page requests, bypassing anti-bot measures and ensuring 100% data
              retrieval reliability.
            </li>
            <li className="mb-[4px]">
              <strong>Secure Networking:</strong> Established a private
              management layer via
              <strong>Tailscale</strong> for encrypted node-to-node connectivity
              and secure remote server administration.
            </li>
            <li className="mb-[4px]">
              <strong>Automation Core:</strong> Leveraged
              <strong>n8n</strong> to synchronize Telegram Bot interactions with
              <strong>PostgreSQL</strong> and AI-based processing nodes.
            </li>
          </ul>
        </li>
      </ul>
    </section>
  );
}
export default Projects;
