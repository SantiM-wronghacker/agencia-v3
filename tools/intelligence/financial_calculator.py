from tools.base import BaseTool, ToolResult, tool


@tool
class FinancialCalculatorTool(BaseTool):
    name = "financial_calculator"
    description = (
        "Realiza cálculos financieros. "
        "Úsala para ROI, VPN, punto de equilibrio, "
        "amortización y análisis de inversiones."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "calculate_roi":
            return self._calculate_roi(**kwargs)
        if action == "calculate_npv":
            return self._calculate_npv(**kwargs)
        if action == "calculate_break_even":
            return self._calculate_break_even(**kwargs)
        if action == "amortization_table":
            return self._amortization_table(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _calculate_roi(
        self,
        investment: float = 0.0,
        returns: float = 0.0,
        period_years: float = 1.0,
    ) -> ToolResult:
        if investment <= 0:
            return self._error("La inversión debe ser mayor a 0")
        roi = ((returns - investment) / investment) * 100
        roi_annual = roi / period_years if period_years > 0 else roi
        payback_months = (
            investment / (returns / (period_years * 12))
            if returns > 0 and period_years > 0
            else float("inf")
        )
        payback_str = (
            f"{payback_months:.1f} meses"
            if payback_months != float("inf")
            else "N/A (retorno negativo)"
        )
        return self._success(
            f"ROI: {roi:.2f}%\n"
            f"ROI Anualizado: {roi_annual:.2f}%\n"
            f"Recuperación: {payback_str}\n"
            f"Ganancia neta: ${returns - investment:,.2f}",
            raw_data={
                "roi": roi,
                "roi_annual": roi_annual,
                "net_gain": returns - investment,
            },
        )

    def _calculate_npv(
        self,
        cashflows: list = None,
        discount_rate: float = 0.10,
        initial_investment: float = 0.0,
    ) -> ToolResult:
        if cashflows is None or not cashflows:
            return self._error("Se requieren flujos de caja (cashflows)")
        npv = -initial_investment
        for i, cf in enumerate(cashflows, 1):
            npv += cf / ((1 + discount_rate) ** i)
        irr_approx = (
            (sum(cashflows) / len(cashflows) / initial_investment * 100)
            if initial_investment > 0
            else 0
        )
        viable = npv > 0
        return self._success(
            f"VPN (NPV): ${npv:,.2f}\n"
            f"TIR aproximada: {irr_approx:.1f}%\n"
            f"{'Proyecto viable (VPN > 0)' if viable else 'Proyecto no viable (VPN ≤ 0)'}",
            raw_data={"npv": npv, "cashflows": cashflows, "viable": viable},
        )

    def _calculate_break_even(
        self,
        fixed_costs: float = 0.0,
        variable_cost_per_unit: float = 0.0,
        price_per_unit: float = 0.0,
    ) -> ToolResult:
        if price_per_unit <= variable_cost_per_unit:
            return self._error(
                "El precio por unidad debe ser mayor al costo variable"
            )
        contribution_margin = price_per_unit - variable_cost_per_unit
        break_even_units = fixed_costs / contribution_margin
        break_even_revenue = break_even_units * price_per_unit
        cm_pct = (contribution_margin / price_per_unit) * 100
        return self._success(
            f"Punto de equilibrio: {break_even_units:.0f} unidades\n"
            f"Ingresos en equilibrio: ${break_even_revenue:,.2f}\n"
            f"Margen de contribución: ${contribution_margin:.2f}/unidad\n"
            f"Margen de contribución %: {cm_pct:.1f}%",
            raw_data={
                "units": break_even_units,
                "revenue": break_even_revenue,
                "contribution_margin": contribution_margin,
            },
        )

    def _amortization_table(
        self,
        principal: float = 0.0,
        annual_rate: float = 0.0,
        periods: int = 12,
        periods_per_year: int = 12,
    ) -> ToolResult:
        if principal <= 0:
            return self._error("El capital debe ser mayor a 0")
        if periods <= 0:
            return self._error("Los períodos deben ser mayor a 0")
        monthly_rate = annual_rate / periods_per_year
        if monthly_rate == 0:
            payment = principal / periods
        else:
            payment = (
                principal
                * (monthly_rate * (1 + monthly_rate) ** periods)
                / ((1 + monthly_rate) ** periods - 1)
            )
        table = []
        balance = principal
        for i in range(1, min(periods + 1, 13)):
            interest = balance * monthly_rate
            principal_paid = payment - interest
            balance = max(0.0, balance - principal_paid)
            table.append(
                f"Período {i}: Pago ${payment:.2f} | "
                f"Capital ${principal_paid:.2f} | "
                f"Interés ${interest:.2f} | "
                f"Saldo ${balance:.2f}"
            )
        if periods > 12:
            table.append(f"... ({periods - 12} períodos más)")
        total_paid = payment * periods
        return self._success(
            f"Pago mensual: ${payment:.2f}\n"
            f"Total a pagar: ${total_paid:.2f}\n"
            f"Total intereses: ${payment * periods - principal:.2f}\n\n"
            + "\n".join(table),
            raw_data={"payment": payment, "total_paid": total_paid},
        )
