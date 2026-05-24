from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ast
import operator

app = FastAPI(title="Calculator API", version="1.0")

# in-memory state for the current expression
_state = {"expression": None, "result": None}

_ops = {
    ast.Add:  operator.add,
    ast.Sub:  operator.sub,
    ast.Mult: operator.mul,
    ast.Div:  operator.truediv,
    ast.Pow:  operator.pow,
    ast.Mod:  operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def _safe_eval(expr: str) -> float:
    # используем ast вместо eval() — не даем выполнить произвольный код
    def _eval(node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError(f"unsupported constant: {type(node.value)}")
        if isinstance(node, ast.BinOp):
            op_fn = _ops.get(type(node.op))
            if not op_fn:
                raise ValueError(f"unsupported operator: {type(node.op).__name__}")
            l, r = _eval(node.left), _eval(node.right)
            if isinstance(node.op, ast.Div) and r == 0:
                raise ValueError("division by zero")
            return op_fn(l, r)
        if isinstance(node, ast.UnaryOp):
            op_fn = _ops.get(type(node.op))
            if not op_fn:
                raise ValueError(f"unsupported unary op: {type(node.op).__name__}")
            return op_fn(_eval(node.operand))
        raise ValueError(f"unsupported node type: {type(node).__name__}")

    try:
        tree = ast.parse(expr.strip(), mode="eval")
    except SyntaxError as e:
        raise ValueError(f"syntax error in expression: {e}")
    return _eval(tree.body)


# --- базовые арифметические операции ---

@app.get("/add")
async def add(a: float, b: float):
    return {"result": a + b}

@app.get("/subtract")
async def subtract(a: float, b: float):
    return {"result": a - b}

@app.get("/multiply")
async def multiply(a: float, b: float):
    return {"result": a * b}

@app.get("/divide")
async def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="division by zero")
    return {"result": a / b}


# --- работа с выражением через состояние ---

class ExprBody(BaseModel):
    expression: str

@app.post("/expression/set")
async def set_expression(body: ExprBody):
    """Сохраняет выражение в состоянии. Принимает строку вида (a+b)*c + (d-e)/(f-g)."""
    _state["expression"] = body.expression
    _state["result"] = None
    return {"expression": _state["expression"], "status": "set"}

@app.get("/expression/current")
async def current_expression():
    """Возвращает текущее выражение и результат последнего вычисления."""
    if _state["expression"] is None:
        raise HTTPException(status_code=404, detail="no expression set")
    return _state

@app.post("/expression/evaluate")
async def evaluate_stored():
    """Вычисляет сохранённое выражение и сохраняет результат в состоянии."""
    if _state["expression"] is None:
        raise HTTPException(status_code=404, detail="no expression set")
    try:
        result = _safe_eval(_state["expression"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    _state["result"] = result
    return {"expression": _state["expression"], "result": result}


# --- inline: вычислить выражение без сохранения состояния ---

@app.get("/evaluate")
async def evaluate_inline(expression: str):
    """Принимает выражение как query-параметр и сразу возвращает результат."""
    try:
        result = _safe_eval(expression)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"expression": expression, "result": result}
