# Love Project

A digital collection of romantic gestures and animations.

## Web Experience
The main experience is a web-based interactive flow.

- **Login (`index.html`)**: The entry point. It asks "What do I call you?".
  - **Correct Answer**: `chiquita` (Redirects to the surprise)
  - **Incorrect Answer**: Redirects to a polite rejection page.
- **The Surprise (`love.html`)**: A beautiful, animated display of roses forming hearts and the message "I LOVE YOU".
- **Rejection (`failure.html`)**: A fallback page for intended visitors only.

### How to Run
Simply open `index.html` in your web browser.

```bash
xdg-open index.html
```

## CLI Experience
For a terminal-based visual treat, included is a Python script that draws growing hearts in the console.

### How to Run
```bash
python3 love.py
```

## Project Structure
- `index.html`: Login / Landing page.
- `love.html`: Main animation page.
- `failure.html`: Access denied page.
- `love.py`: Terminal animation script.
- `pydancer/`: Additional Python resources.
