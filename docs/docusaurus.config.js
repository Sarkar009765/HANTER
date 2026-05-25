module.exports = {
    title: "HANTER",
    tagline: "Personal AI Agent Framework",
    url: "https://HANTER.dev",
    baseUrl: "/",
    onBrokenLinks: "throw",
    onBrokenMarkdownLinks: "warn",
    favicon: "img/favicon.ico",
    organizationName: "HANTER",
    projectName: "HANTER",
    presets: [
        [
            "classic",
            {
                docs: {
                    sidebarPath: undefined,
                    editUrl: "https://github.com/Sarkar009765/HANTER/edit/main/docs/",
                },
                theme: {
                    customCss: [],
                },
            },
        ],
    ],
    themeConfig: {
        navbar: {
            title: "HANTER",
            items: [
                { to: "/docs/intro", label: "Docs", position: "left" },
                { to: "/docs/installation", label: "Install", position: "left" },
                { to: "/docs/architecture", label: "Architecture", position: "left" },
                {
                    href: "https://github.com/Sarkar009765/HANTER",
                    label: "GitHub",
                    position: "right",
                },
            ],
        },
        footer: {
            style: "dark",
            links: [
                {
                    title: "Docs",
                    items: [
                        { label: "Getting Started", to: "/docs/intro" },
                        { label: "Installation", to: "/docs/installation" },
                        { label: "Architecture", to: "/docs/architecture" },
                    ],
                },
                {
                    title: "Community",
                    items: [
                        { label: "Discord", href: "https://discord.gg/hanter" },
                        { label: "GitHub", href: "https://github.com/Sarkar009765/HANTER" },
                    ],
                },
            ],
            copyright: `Copyright © ${new Date().getFullYear()} HANTER. MIT Licensed.`,
        },
    },
};
