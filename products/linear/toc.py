from shared.types import TocItem

BASE_URL = "https://linear.app"

NAV_STRUCTURE = [
    {"section": "Getting started", "pages": [
        ("Start Guide", "/docs/start-guide"),
        ("Concepts", "/docs/conceptual-model"),
        ("Download Linear", "/docs/get-the-app"),
    ]},
    {"section": "Account", "pages": [
        ("Profile", "/docs/profile"),
        ("Preferences", "/docs/account-preferences"),
        ("Notifications", "/docs/notifications"),
        ("Security & Access", "/docs/security-and-access"),
    ]},
    {"section": "Your sidebar", "pages": [
        ("Inbox", "/docs/inbox"),
        ("My issues", "/docs/my-issues"),
        ("Pulse", "/docs/pulse"),
        ("Pull Request Reviews", "/docs/pull-request-reviews"),
        ("Favorites", "/docs/favorites"),
    ]},
    {"section": "Teams", "pages": [
        ("Teams", "/docs/teams"),
        ("Private teams", "/docs/private-teams"),
        ("Sub-teams", "/docs/sub-teams"),
        ("Issue status", "/docs/configuring-workflows"),
    ]},
    {"section": "Issues", "pages": [
        ("Create issues", "/docs/creating-issues"),
        ("Edit issues", "/docs/editing-issues"),
        ("Assign and delegate issues", "/docs/assigning-issues"),
        ("Select issues", "/docs/select-issues"),
        ("Parent and sub-issues", "/docs/parent-and-sub-issues"),
        ("Issue templates", "/docs/issue-templates"),
        ("Issue documents", "/docs/issue-documents"),
        ("Comments and reactions", "/docs/comment-on-issues"),
        ("Editor", "/docs/editor"),
        ("Delete and archive issues", "/docs/delete-archive-issues"),
        ("Customer Requests", "/docs/customer-requests"),
    ]},
    {"section": "Issue properties", "pages": [
        ("Due dates", "/docs/due-dates"),
        ("Estimates", "/docs/estimates"),
        ("Issue relations", "/docs/issue-relations"),
        ("Labels", "/docs/labels"),
        ("Priority", "/docs/priority"),
        ("SLAs", "/docs/sla"),
    ]},
    {"section": "Projects", "pages": [
        ("Projects", "/docs/projects"),
        ("Initiative and Project updates", "/docs/initiative-and-project-updates"),
        ("Project milestones", "/docs/project-milestones"),
        ("Project overview", "/docs/project-overview"),
        ("Project documents", "/docs/project-documents"),
        ("Project graph", "/docs/project-graph"),
        ("Project status", "/docs/project-status"),
        ("Project labels", "/docs/project-labels"),
        ("Project notifications", "/docs/project-notifications"),
        ("Project priority", "/docs/project-priority"),
        ("Project dependencies", "/docs/project-dependencies"),
        ("Project templates", "/docs/project-templates"),
    ]},
    {"section": "Initiatives", "pages": [
        ("Initiatives", "/docs/initiatives"),
        ("Sub-initiatives", "/docs/sub-initiatives"),
    ]},
    {"section": "Cycles", "pages": [
        ("Cycles", "/docs/use-cycles"),
        ("Update cycles", "/docs/update-cycles"),
        ("Cycle graph", "/docs/cycle-graph"),
    ]},
    {"section": "Views", "pages": [
        ("Board layout", "/docs/board-layout"),
        ("Timeline", "/docs/timeline"),
        ("Custom Views", "/docs/custom-views"),
        ("Triage", "/docs/triage"),
        ("User views", "/docs/user-views"),
        ("Peek preview", "/docs/peek"),
        ("Team pages", "/docs/default-team-pages"),
        ("Label views", "/docs/label-views"),
    ]},
    {"section": "Find and filter", "pages": [
        ("Search", "/docs/search"),
        ("Filters", "/docs/filters"),
        ("Display options", "/docs/display-options"),
    ]},
    {"section": "AI", "pages": [
        ("AI Agents", "/docs/agents-in-linear"),
        ("MCP server", "/docs/mcp"),
        ("Triage Intelligence", "/docs/triage-intelligence"),
    ]},
    {"section": "Integrations", "pages": [
        ("Integration Directory", "/docs/integration-directory"),
        ("Airbyte", "/docs/airbyte"),
        ("Asks", "/docs/linear-asks"),
        ("Discord", "/docs/discord"),
        ("Figma", "/docs/figma"),
        ("Front", "/docs/front"),
        ("GitHub", "/docs/github-integration"),
        ("GitLab", "/docs/gitlab"),
        ("Google Sheets", "/docs/google-sheets"),
        ("Gong", "/docs/gong"),
        ("Intercom", "/docs/intercom"),
        ("Jira", "/docs/jira"),
        ("Microsoft Teams", "/docs/microsoft-teams"),
        ("Notion", "/docs/notion"),
        ("Salesforce", "/docs/salesforce"),
        ("Sentry", "/docs/sentry"),
        ("Slack", "/docs/slack"),
        ("Zapier", "/docs/zapier"),
        ("Zendesk", "/docs/zendesk"),
    ]},
    {"section": "Analytics", "pages": [
        ("Dashboards", "/docs/dashboards"),
        ("Insights", "/docs/insights"),
        ("Exporting Data", "/docs/exporting-data"),
    ]},
    {"section": "Administration", "pages": [
        ("Workspaces", "/docs/workspaces"),
        ("Login methods", "/docs/login-methods"),
        ("Invite members", "/docs/invite-members"),
        ("Members and roles", "/docs/members-roles"),
        ("Security", "/docs/security"),
        ("SAML", "/docs/saml-and-access-control"),
        ("SCIM", "/docs/scim"),
        ("API and Webhooks", "/docs/api-and-webhooks"),
        ("Third-Party App Approvals", "/docs/third-party-application-approvals"),
        ("Billing and plans", "/docs/billing-and-plans"),
        ("Audit log", "/docs/audit-log"),
        ("Importer", "/docs/import-issues"),
    ]},
]


def get_toc_items() -> list[TocItem]:
    """Build flat TOC list with section dividers."""
    items = []
    seen_hrefs = set()

    for group in NAV_STRUCTURE:
        items.append(TocItem(
            type="section",
            title=group["section"],
            url=None,
            section=group["section"],
        ))

        for title, href in group["pages"]:
            if href in seen_hrefs:
                continue
            seen_hrefs.add(href)
            items.append(TocItem(
                type="page",
                title=title,
                url=f"{BASE_URL}{href}",
                section=group["section"],
            ))

    return items
