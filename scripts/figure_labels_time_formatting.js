
// Add time labels to 3 decimal places like "1.234 s"

figureModel.getSelected().forEach(p => {
    let theT = p.get('theT');
    let deltaT = p.get('deltaT')?.[theT];
    console.log("deltaT", deltaT);
    if (deltaT == undefined) return;
    p.add_labels([{
        text: deltaT.toFixed(3) + " s",
        size: 14,
        position: 'topleft',
        color: 'ffffff'
    }]);
});
