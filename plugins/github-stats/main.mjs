// github-stats — public GitHub REST API queries. Unauthenticated, so
// you get the 60-req/hr quota per IP. That's fine for "how popular is
// this repo" questions.
//
// Inspired by lobe-chat-plugins' `gitUserRepoStats`. No remote
// dependency; uses the official api.github.com endpoint.

const BASE = "https://api.github.com";

export function activate(context) {
  const repoHandle = context.tools.register("get_repo", {
    description:
      "Look up a public GitHub repository by `owner/repo` and return its " +
      "stars, forks, open issues, primary language, license, default branch, " +
      "last push, and homepage. Anonymous request — hits the 60/hr/IP quota.",
    parameters: {
      type: "object",
      properties: {
        repo: {
          type: "string",
          description: "`owner/repo`, e.g. `vercel/next.js`.",
        },
      },
      required: ["repo"],
    },
    execute: async (args = {}) => {
      const { repo } = args ?? {};
      if (typeof repo !== "string" || !/^[\w.-]+\/[\w.-]+$/.test(repo)) {
        throw new Error("`repo` must be in `owner/repo` form.");
      }
      const data = await ghFetch(`/repos/${repo}`);
      return {
        fullName: data.full_name,
        description: data.description,
        stars: data.stargazers_count,
        forks: data.forks_count,
        openIssues: data.open_issues_count,
        language: data.language,
        license: data.license?.spdx_id ?? null,
        defaultBranch: data.default_branch,
        homepage: data.homepage || null,
        url: data.html_url,
        topics: data.topics ?? [],
        pushedAt: data.pushed_at,
        archived: data.archived === true,
        isFork: data.fork === true,
      };
    },
  });

  const userHandle = context.tools.register("get_user", {
    description:
      "Look up a public GitHub user or organization by login and return their " +
      "bio, location, public repo count, followers, and profile URL.",
    parameters: {
      type: "object",
      properties: {
        login: { type: "string", description: "GitHub username or org name." },
      },
      required: ["login"],
    },
    execute: async (args = {}) => {
      const { login } = args ?? {};
      if (typeof login !== "string" || !/^[\w-]+$/.test(login)) {
        throw new Error("`login` must be a valid GitHub username.");
      }
      const data = await ghFetch(`/users/${login}`);
      return {
        login: data.login,
        name: data.name,
        type: data.type,
        bio: data.bio,
        company: data.company,
        location: data.location,
        blog: data.blog,
        publicRepos: data.public_repos,
        followers: data.followers,
        following: data.following,
        url: data.html_url,
        createdAt: data.created_at,
      };
    },
  });

  return {
    dispose: () => {
      repoHandle.dispose();
      userHandle.dispose();
    },
  };
}

async function ghFetch(path) {
  const response = await fetch(`${BASE}${path}`, {
    headers: {
      Accept: "application/vnd.github+json",
      "User-Agent":
        "Trapezohe-Ghast/0.1 (+https://ghast.trapezohe.ai) github-stats",
    },
  });
  if (response.status === 403) {
    throw new Error(
      "GitHub API rate limit reached (60/hr for anonymous). Try again in an hour.",
    );
  }
  if (response.status === 404) {
    throw new Error("Not found on GitHub.");
  }
  if (!response.ok) {
    throw new Error(`GitHub API ${response.status} ${response.statusText}`);
  }
  return response.json();
}
