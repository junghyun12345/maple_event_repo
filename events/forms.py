from django import forms
from django.forms import inlineformset_factory

from .models import Event, Reward


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title", "slug", "category", "start_at", "end_at",
            "thumbnail", "summary_short", "summary_three",
            "body", "source_url", "is_published",
        ]
        widgets = {
            "start_at": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "end_at": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "summary_three": forms.Textarea(attrs={"rows": 3}),
            "body": forms.Textarea(attrs={"rows": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ("start_at", "end_at"):
            self.fields[f].input_formats = ["%Y-%m-%dT%H:%M"]
        for field in self.fields.values():
            w = field.widget
            if isinstance(w, forms.CheckboxInput):
                w.attrs["class"] = "checkbox"
            elif isinstance(w, forms.Select):
                w.attrs["class"] = "select select-bordered w-full"
            elif isinstance(w, forms.Textarea):
                w.attrs["class"] = "textarea textarea-bordered w-full"
            else:
                w.attrs["class"] = "input input-bordered w-full"


class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ["name", "quantity", "condition", "order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "input input-bordered input-sm w-full"


# 이벤트(부모)에 딸린 보상(자식)들을 함께 다루는 inline formset.
RewardFormSet = inlineformset_factory(
    Event,
    Reward,
    form=RewardForm,
    extra=1,          # 기본으로 빈 입력줄 1개
    can_delete=True,  # 기존 보상 삭제 체크박스
)
