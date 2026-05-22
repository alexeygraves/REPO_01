describe('About Assignment (about_assignment.js)', function() {
  it('local variables', function() {
    let temp = 1;
    expect(temp).toBe(1);
  });

  it('global variables', function() {
    temp = 1;
    expect(window.temp).toBe(temp);
  });
});
