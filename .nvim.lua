require("conform").setup({
	formatters_by_ft = {
		python = { "isort", "black" },
        javascript = { { "prettierd", "prettier" } },
	},
})