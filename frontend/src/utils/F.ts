export class F{
    static canvasWidth(): number{
        const max = 600;
        const w = window.innerWidth > window.innerHeight && window.innerWidth > max
            ? max
            : window.innerWidth;
        return w - (window.innerWidth*.05);
    }
}