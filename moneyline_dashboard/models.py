from django.db import models

# Create your models here.
class SportsEvent(models.Model):
    name = models.CharField("Name",max_length=255,unique=True)
    game_datetime = models.DateTimeField("Game Time")
    observation_datetime = models.DateTimeField("Last Updated")
    league = models.CharField("League",max_length=255)
    home_team = models.CharField("Home Team",max_length=255)
    away_team = models.CharField("Away Team",max_length=255)
    home_win_prob = models.DecimalField("Home Win Probability", max_digits=10, decimal_places=6)
    away_win_prob = models.DecimalField("Away Win Probability", max_digits=10, decimal_places=6)
    win_prob_history = models.JSONField(blank=True,null=True)
    closed = models.BooleanField(default=False)
    settled = models.BooleanField(default=False)
    home_score = models.IntegerField("Home Score",blank=True,null=True)
    away_score = models.IntegerField("Away Score",blank=True,null=True)
    winning_team = models.CharField("Winner",max_length=255,blank=True,null=True)

    def best_line(self):
        best_line = BettingLine.objects.filter(game=self).order_by('-expected_roi')[0]
        return best_line

    def matchup(self):
        return self.away_team + " @ " + self.home_team

    def update_outcome(self):
        if self.settled:
            if self.home_score > self.away_score:
                self.winning_team = self.home_team
                self.save()
            elif self.home_score < self.away_score:
                self.winning_team = self.away_team
                self.save()

    def __str__(self):
        return self.game_datetime.strftime("%Y-%m-%d ") + self.matchup()

class BettingLine(models.Model):
    game = models.ForeignKey(SportsEvent,related_name="betting_lines",on_delete=models.CASCADE)
    observation_datetime = models.DateTimeField("Last Updated")
    sportsbook = models.CharField("Sportsbook",max_length=255)
    side = models.CharField("Side",max_length=255)
    hit_prob = models.DecimalField("Hit Probability", max_digits=10, decimal_places=6)
    odds = models.DecimalField("Odds", max_digits=10, decimal_places=6)
    expected_roi = models.DecimalField("Expected ROI", max_digits=10, decimal_places=6)

    def __str__(self):
        return self.side + ' - ' + self.sportsbook
